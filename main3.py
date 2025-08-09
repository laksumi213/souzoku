import pyautogui
from flet import (
    app,
    Page,
    colors,
    Container,
    Text,
)
import os
from components.layout import MyLayout
from components.body import HomeBody
from components.body import SettingsBody
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    username1 = Column(String)


# class Task(Base):
#     __tablename__ = 'tasks'
#     id = Column(Integer, primary_key=True)
#     description = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='tasks')


engine = create_engine('sqlite:///' + os.path.dirname(__file__) + '/db/inheritance.db',  echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
users = session.query(User).all()
# with Session() as session:
#     user = session.query(User).all()
print(users)

# import sqlite3
# sql = 'select * from customer'
# dbname = 'inheritance.db'
# conn = sqlite3.connect(dbname)
# cur = conn.cursor()
# records = cur.execute(sql).fetchall()
# print(records)
# conn.close()


# SQLiteの場合
# engine = create_engine('sqlite:///inheritance.db')
# Session = sessionmaker(bind=engine)
# session = Session()
# session = sessionmaker(bind=create_engine('sqlite:///inheritance.db'))
# # results = session.query(User).filter(User.age >= 20).all()
# users = User.query.all()
# print(users)


def main(page: Page):
    def route_change(e):
        print()
        print("route_change:", e, )

        if page.session.get('page_count') == 0:
            page.session.set('page_count', int(page.session.get('page_count')) + 1)
        else:
            # before_root = page.session.get(f'before_route_{page.session.get('page_count')}')
            # print(f'before_route_{page.session.get('page_count')}', before_root)
            # page.session.set(f'before_route_{page.session.get('page_count')}', before_root)
            page.session.set('page_count', int(page.session.get('page_count')) + 1)

        # if page.session.get('page_count') is not None:
        #     before_root = page.session.get(f'before_route_{page.session.get('page_count')}')
        #     page.session.set(f'before_route_{page.session.get('page_count')}', before_root)
        #     print(f'before_route_{page.session.get('page_count')}:', before_root)
        #
        #     page.session.set('page_count', int(page.session.get('page_count')) + 1)
        #     print("page.session.get('page_count'):", page.session.get('page_count'))
        #
        # else:
        #     page.session.set('page_count', 0)
        #     before_root = '/home'

        # before_bodyを変更前にセッションにセット
        # page.session.set(f'before_route_{page.session.get('page_count')}', main_body.content)
        # page.session.set(f'before_body_{int(page.session.get('page_count'))}', main_body.content)

        # print('before_root:', before_root)
        # page.session.set(f'before_route_{page.session.get('page_count')}', before_root)

        main_body.content = page.session.get(page.route)

        # if page.route == "/home":
        #     main_body.content = page.session.get('/home')
        #
        # elif page.route == "/home/procedure":
        #     main_body.content = Text("Settings Page", size=30)
        #
        # elif page.route == "/settings":
        #     main_body.content = page.session.get('/settings')

        page.update()

    # def main
    main_body = Container(
        content=HomeBody(page),
        expand=True,  # 残りのスペースを埋める
    )
    page.session.set('main_body', main_body)
    # before_route = {'/home'}
    # page.session.set('before_route', before_route)
    # page.session.set('settings_body', SettingsBody(page))
    page.session.set('/home', HomeBody(page))
    page.session.set('/home/procedure', Text("Settings Page", size=30))
    page.session.set('/settings', SettingsBody(page))
    page.session.set('page_count', 0)
    # page.session.set('page_count', None)

    page.title = '遺言・相続手続きシステム'
    # page.padding = 10
    page.scrollTo = "always"
    page.scroll = 'always'
    page.bgcolor = colors.AMBER_50
    page.window_top = 0
    page.window_left = 0
    page.window_height = pyautogui.size().height
    page.window_width = pyautogui.size().width
    # page.window_maximized = True
    # page.window_center()
    # page.window_minimizable = True
    # page.window_maximizable = True
    # page.window_resizable = True
    page.on_route_change = route_change
    page.add(MyLayout(page))
    page.go("/home")


if __name__ == "__main__":
    app(target=main)
