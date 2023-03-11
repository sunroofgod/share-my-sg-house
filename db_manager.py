import os
from dotenv import load_dotenv
from sqlalchemy import text, DDL, event
import sqlalchemy

load_dotenv('.env')
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
CONNECTION_STRING = f"postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/ShareMySGHouse"
NUM_OF_TABLES = 5
engine = sqlalchemy.create_engine(
    CONNECTION_STRING
)
db = engine.connect()

def create_all_tables(db: sqlalchemy.engine.Connection) -> None:
    db.execute(text(
        '''CREATE TABLE IF NOT EXISTS users(
            email VARCHAR(32) PRIMARY KEY,
            fname VARCHAR(32) NOT NULL,
            lname VARCHAR(32) NOT NULL,
            age INTEGER NOT NULL)'''
    ))
    db.execute(text(
        '''CREATE TABLE IF NOT EXISTS houses(
            id INTEGER PRIMARY KEY,
            location VARCHAR(32) NOT NULL,
            price FLOAT NOT NULL,
            num_room INTEGER NOT NULL)'''
    ))
    db.execute(text(
        '''CREATE TABLE IF NOT EXISTS credit_cards(
            type VARCHAR(20) PRIMARY KEY,
            number VARCHAR(32) NOT NULL,
            email VARCHAR(32) NOT NULL)'''
    ))
    db.execute(text(
        '''CREATE TABLE IF NOT EXISTS rental(
            email VARCHAR(32),
            houseid INTEGER,
            num_of_days INTEGER NOT NULL,
            date DATE NOT NULL,
            PRIMARY KEY(email, houseid))'''
    ))
    db.execute(text(
        '''CREATE TABLE IF NOT EXISTS house_ratings(
            email VARCHAR(32),
            houseid INTEGER,
            rating INTEGER NOT NULL,
            date DATE NOT NULL,
            PRIMARY KEY(date, houseid))'''
    ))
    db.commit()
    print("ALL TABLES CREATED SUCCESSFULLY")

def load_dummy_data(db: sqlalchemy.engine.Connection) -> None:
    pass

def check_table_exist(db: sqlalchemy.engine.Connection) -> bool:
    res = db.execute(text(
            '''SELECT count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public'
            '''
        ))
    return res.scalar() == NUM_OF_TABLES

def setup_database(db: sqlalchemy.engine.Connection) -> None:
    if (check_table_exist(db)):
        return
    # if tables do not exist
    # create them
    create_all_tables(db)
    load_dummy_data(db)