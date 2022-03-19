from hashlib import md5
from helpers.decorators import except_handler
from models import User


class Auth:

    @except_handler('При авторизации возникла ошибка')
    def login(self):
        try:
            print('Авторизаця:')
            login = input('Login: ')
            password = input('Password: ')
            user = User.get(User.login == login)
            if not user or self.__password_comparison(user.password, password):
                raise Exception('Данные не верны')
        except Exception as e:
            print(e)
            self.login()

    def __password_comparison(self, db_password, password):
        if (md5(password.encode('utf-8')).hexdigest() != db_password):
            return True
        else:
            return False