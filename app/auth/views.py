from flask import render_template, session, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app.forms import loginForm
from app.firestore_service import get_user, user_put
# Estamos importando auth.
from . import auth
from app.models import UserData, UserModel

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # vamos a renderear la forma de login.
    login_form = loginForm()
    context = {
        'login_form': login_form,
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        # Entonces sacamos el usuario.
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password == password_from_db:
                # Si es el mismo password, entonces lo que haremos sera
                # crear nuestro user model y userdata.
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                # Vamos a hacer login con este userModel, que tendra las propiedades del Mixin
                # y de nuestro UserModel.
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La informacion proporcionada no coincide')
        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))
        
    return render_template('login.html', **context)

# Le diremos que tenemos una ruta de auth
@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
# Aceptamos ambos metodos, por que get obtiene la forma y post la envia
def signup():
    signup_form = loginForm()

    context = {
        'signup_form': signup_form,
    }
    if signup_form.validate_on_submit():
        # Veremos si existe el usuario.
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)
        # Obtenemos al usuario
        if user_doc.to_dict() is None:
            # si el usuario es none, entonces vamos a generar un password hash de lo que nos envia el usuario.
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe')
    return render_template('signup.html', **context)