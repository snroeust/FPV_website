import os
from mock import ip_seg_dic
#from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))




class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')


    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://snroeust:fpvhdde@34.107.64.143/neu?unix_socket=/cloudsql/secret-lambda-262218:europe-west3:fpvhdde'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['eustergerling.ro@gmail.com']
    SERVER_NAME = '192.168.1.2:5000'


    JOBS = [
        {
            'id': 'tcp_handler',
            'func': 'website:start_tcp_Connections',
            'args': (),
            'max_instances': 12
        },

        {
            'id': 'udp_handler',
            'func': 'website:start_udp_Connections',
            'args': (),
            'max_instances': 12
        }


    ]
    SCHEDULER_API_ENABLED = True

    POSTS_PER_PAGE = 10



