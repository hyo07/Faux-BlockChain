# coding: utf-8
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME, BOOLEAN
import sys
import os

# sqliteの設定
dir_name = os.path.dirname(__file__)
sqlite_path = dir_name + "/test.sqlite3"
ENGINE = create_engine('sqlite:///{}'.format(sqlite_path))

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

Base = declarative_base()
Base.query = session.query_property()


class BlockChain(Base):
    __tablename__ = 'block_chain'
    index = Column('index', Integer, primary_key=True, autoincrement=True)
    prev_hash = Column('prev_hash', String, unique=True, nullable=True)
    time_stamp = Column('time_stamp', DATETIME, autoincrement=False)
    user_name = Column('user_name', String, unique=False, autoincrement=False, nullable=True)
    message = Column('message', String, unique=False, autoincrement=False, nullable=True)
    nonce = Column('nonce', INTEGER, unique=False, autoincrement=False)
    genesis_block = Column('genesis_block', BOOLEAN, unique=False, autoincrement=False, nullable=True)


def main(args):
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)
