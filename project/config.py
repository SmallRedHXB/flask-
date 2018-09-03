import os
import pymysql
pymysql.install_as_MySQLdb()
DEBUG=True

SECRET_KEY = os.urandom(24)

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'flask_project'
USERNAME = 'root'
PASSWORD = 'h18067938112'

DB_URL = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = True

