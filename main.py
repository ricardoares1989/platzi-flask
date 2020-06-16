from flask import Flask, request, make_response, redirect, render_template


app = Flask(__name__)
to_dos = ['TODO1', 'TODO2', 'TODO3']


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    # Aqui vamosa a regresar una respuesta de flag.
    # Tenemos que modificar nuestra ruta hello para que obtenga la ruta desde las cookies.
    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip':user_ip,
        'to_dos': to_dos,
    }
    return render_template('hello.html', **context)
