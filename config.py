import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jstar_designers_byjojo'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jstar_designers.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False