import app.utils as utils
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, text, bindparam, select

# engine = create_engine('sqlite:///' + utils.get_database_path(), echo=True)
engine = create_engine('sqlite:///' + utils.get_database_path(), echo=False)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
        # print('session_scope try')
    except:
        session.rollback()
        # print('session_scope except')
        raise
    finally:
        # print('session_scope finally')
        session.close()


def get_db_sql(sql, key=None, para=None):
    with engine.connect() as conn:
        stmt = text(sql)
        if key is not None:
            stmt = stmt.bindparams(bindparam(key))
            # stmt = stmt.bindparams(bindparam(key, type_=Integer))
            results = conn.execute(stmt, {key: para}).mappings().all()
        else:
            results = conn.execute(stmt).mappings().all()
        return results


# def get_db_query(table, key='', para=''):
#     with session_scope() as session:
#         return session.query(Heir).filter(Heir.code == '2412001').all()


Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    username1 = Column(String)


class Heir(Base):
    __tablename__ = 'heir'
    heir_id = Column(Integer, primary_key=True)
    code = Column()
    username1 = Column(String)
    username2 = Column(String)
    username1_hurigana = Column(String)


# with session_scope() as session:
#     heirs = session.query(Heir).all()
#     for heir in heirs:
#         print(f"ID: {heir.heir_id}, Name: {heir.username1} {heir.username2}")

# with session_scope() as session:
#     young_users = session.query(User).filter(User.age < 30).all()
#     for user in young_users:
#         print(f"Name: {user.name}, Age: {user.age}")
#
# with session_scope() as session:
#     user = session.query(User).filter(User.name == "Alice").first()
#     if user:
#         print(f"Found: {user.name}, Age: {user.age}")
#
# from sqlalchemy import text
#
# with session_scope() as session:
#     result = session.execute(text("SELECT * FROM users WHERE age > :age"), {"age": 25})
#     for row in result:
#         print(row)

# print(get_db_sql("SELECT * FROM customer WHERE code = :code"))

# with session_scope() as session:
#     results = session.execute(text("SELECT * FROM customer WHERE code = :code"), {'code': '2412001'})
#     for result in results:
#         print(result)


# heirs = get_db_sql(sql="SELECT * FROM heir WHERE code = :code", key='code', para='2412001').fetchall()
# print('heirs:', heirs)
# for heir in heirs:
#     print(heir)


# with engine.connect() as conn:
#     # stmt = text("SELECT heir_id AS id, username1 || username2 AS 氏名 FROM heir")
#     # stmt = text("SELECT username1, username2 FROM heir")
#     # results = conn.execute(stmt).mappings().all()
#     stmt = text("SELECT heir_id AS id, username1 || ' ' || username2 AS 氏名 FROM heir WHERE code = :code")
#     stmt = stmt.bindparams(bindparam("code", type_=Integer))
#     results = conn.execute(stmt, {"code": "2412001"}).mappings().all()
#     print(results[0]['氏名'])


# with session_scope() as session:
#     heirs = session.query(Heir).filter(Heir.code == '2412001').all()
#     for heir in heirs:
#         print(heir.username1, heir.username2)


# with engine.connect() as conn:
#     stmt = text("SELECT * FROM heir WHERE code = :code")
#     stmt = stmt.bindparams(bindparam("code", type_=Integer))
#
#     results = conn.execute(stmt, {"code": "2412001"}).fetchall()
#     print(results)