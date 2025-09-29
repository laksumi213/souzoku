from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import app.utils as utils

engine = create_engine('sqlite:///' + utils.get_database_path(), echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
        # print('session_scope try')
    except:
        session.rollback()
        print('session_scope except')
        raise
    finally:
        session.close()
        # print('session_scope finally')