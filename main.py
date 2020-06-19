import unittest
from flask import request, make_response, redirect, render_template, abort, session, url_for, flash
from flask_login import login_required, login_user, current_user
from app import create_app
from app.forms import loginForm, TodoForm, DeleteTodoForm, UpdateTodoForm

from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo


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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    # login_form = loginForm()
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    context = {
        'user_ip':user_ip,
        'to_dos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }
    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)   
        flash('tarea creada con exito')
        redirect(url_for('hello'))
    return render_template('hello.html', **context)

# para esto vamosa recibir rutas dinamicas de tal modo que recibimos informacion
# como string y numeros
@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


# Done lo vamos a forzar que seaun numero.
@app.route('/todos/delete/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))
