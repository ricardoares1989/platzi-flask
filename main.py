from flask import request, make_response, redirect, render_template, abort, session, url_for, flash
import unittest

from app import create_app
from app.forms import loginForm

app = create_app()

to_dos = ['Comprar cafe', 'Solicitud de compra', 'Entregar video al producto']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(500)
def server_error_found(error):
    return render_template('500.html', error=error)


@app.route('/debug-errors/500')
def error_500():
    abort(500)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET','POST'])
def hello():
    user_ip = session.get('user_ip')
    login_form = loginForm()
    username = session.get('username')
    context = {
        'user_ip':user_ip,
        'to_dos': to_dos,
        'login_form': login_form,
        'username': username,
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con exito')
        return redirect(url_for('index'))
    return render_template('hello.html', **context)
