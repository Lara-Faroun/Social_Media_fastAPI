from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

Base = declarative_base()

#'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'
#SQLALCHEMY_DATABASE_URL ='postgresql://postgres:81222@localhost/fastapi'
#SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}'
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

#The engine is responsible for establishing the connection  
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#We need a a session to talk to the SQL DB
Sessionlocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

#Dependency 
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host = 'localhost' , database='fastapi',user='postgres',
#     password='81222',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database connected successfuly')

# except Exception as error:
#     print(f"Error while connecting to Database {error}")
