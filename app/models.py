from flask_login import UserMixin

from app.firestore_service import get_user

class UserData:
# Esta define la data que se requiere del usuario al iniciarlo.
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data):
        """parame user_data: UserData"""
        self.id = user_data.username
        self.password = user_data.password
    
    # Como sera un emtodo estatico no recibira self.
    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        # Cremos nuestro user_data con su clase respectivamente.
        return UserModel(user_data)