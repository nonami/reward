import os

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}".format(
    DB_USER=os.getenv('DB_USER', 'root'),
    DB_PASS=os.getenv('DB_PASS', 'password'),
    DB_HOST=os.getenv('DB_HOST', '127.0.0.1'),
    DB_NAME=os.getenv('DB_NAME', 'reward_service'),
)

DEBUG = True