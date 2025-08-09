import flet as ft

class CustomTextField(ft.UserControl):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def build(self):
        return ft.TextField(**self.config)

def main(page: ft.Page):
    page.add(
        CustomTextField({"hint_text": "名前を入力", "width": 300, "border_color": ft.colors.GREEN}),
        CustomTextField({"label": "メールアドレス", "keyboard_type": ft.KeyboardType.EMAIL}),
    )

ft.app(target=main)

# import app.database_utils as database_utils
# from sqlalchemy import create_engine, Column, Integer, String, text, bindparam, select

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import declarative_base
#
# Base = declarative_base()
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# # 使用例
# user = User(id=1, name="田中太郎", age=30)
# user_dict = user.to_dict()
# print(user_dict)  # 出力: {'id': 1, 'name': '田中太郎', 'age': 30}


from app.models.models import *

# heirs = Heir.get_all_db(Heir)
# print('heirs:', heirs)

# decedent = Decedent.get_customer_huri(Decedent, 'す')
# # for s in decedent:
# #     print(s.名)
# print('decedent:', decedent[0].名)
# print('decedent:', decedent[1]['名'])
# print('decedent:', decedent)


# heirs = get_all_heirs()
# print('heirs:', heirs)
# for heir in heirs:
#     print(heir.username2)

# with database_utils.session_scope() as session:
#     filters = {
#         'code': ['2412001'],
#         'username2': ['修']
#     }
#
#     # conditions = []
#     # conditions.append(database_utils.Heir.code.in_(filters['code']))
#     # conditions.append(database_utils.Heir.username2.in_(filters['username2']))
#
#     conditions = [database_utils.Heir.code.in_(filters['code']),
#                   database_utils.Heir.username2.in_(filters['username2'])]
#
#     stmt = select(database_utils.Heir).where(*conditions)
#     heirs = session.execute(stmt).scalars().all()
#
#     # heirs = session.query(database_utils.Heir).filter(database_utils.Heir.code == '2412001').all()
#     for heir in heirs:
#         print(heir.username1, heir.username2)
# print(heir.username1, heir.username2)

# sql = "SELECT heir_id AS id, username1 || ' ' || username2 AS 氏名 FROM heir WHERE code = :code"
# results = database_utils.get_db_sql(sql, 'code', '2412001')
# print(results)
# print(results[0]['氏名'])
