import os


class Config(object):
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'trivia'
    DATABASE_CREDENTIALS = os.environ.get('DATABASE_CREDENTIALS') or 'postgres:postgres'
    DATABASE_HOST_PORT = os.environ.get('DATABASE_HOST_PORT') or 'localhost:15432'
    SQLALCHEMY_DATABASE_URI = "postgres://{}@{}/{}".format(DATABASE_CREDENTIALS, DATABASE_HOST_PORT, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTest(object):
    DATABASE_NAME = 'trivia_test'
    DATABASE_CREDENTIALS = 'postgres:postgres'
    DATABASE_HOST_PORT = 'localhost:15432'
    SQLALCHEMY_DATABASE_URI = "postgres://{}@{}/{}".format(DATABASE_CREDENTIALS, DATABASE_HOST_PORT, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
