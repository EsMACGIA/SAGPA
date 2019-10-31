import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Normalmente alchemy anvia una sennal al servidor antes de cada cambio a la base de dato
    # con esto apagamos esa funcion
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = basedir
    TESTING = True
    LOGIN_DISABLED = False