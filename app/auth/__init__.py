from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')
# Esto significa que todas las rutas que empiecen con el prefijo van a
# dirigirse a este Blueprint. Despues hay que crear una vista.

from . import views
# Despues de crear el Blueprint tenemos que colcoar esto.


