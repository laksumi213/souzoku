from sqlalchemy import (
    CHAR,
    Column,
    Date,
    Integer,
    String,
    and_,
    delete,
    func,
    inspect,
    or_,
    select,
)

# from . import Base, engine, session_scope
from app.models import Base, engine, session_scope


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def recreate_all_tables(cls):
        try:
            Base.metadata.drop_all(engine)
            print()
            print("✅ 既存のテーブルを削除しました。")
            print()

            # 2. CREATE ALL: Baseに定義されている全てのテーブルをデータベースに再作成
            Base.metadata.create_all(engine)
            print()
            print("✅ テーブルを新しく作成しました。")
            print()

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")

    @classmethod
    def register_data(cls, model_class, data: dict):
        print(cls)
        print('**data:', data)
        new_record = model_class(**data)
        print('new_record:', new_record)
        with session_scope() as session:
            session.add(new_record)
            print("✅ データの登録とコミットが完了しました。")

    def to_dict(self, results):
        return [
            {c.name: getattr(result, c.name) for c in self.__table__.columns}
            for result in results
        ]

    @classmethod
    def get_table_columns_info(cls, table_name):
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            print(f"エラー: テーブル '{table_name}' は存在しません。")
            return []

        # 1. 主キー制約の情報を取得
        pk_constraint = inspector.get_pk_constraint(table_name)

        # 主キーの列名リストを抽出
        pk_column_names = pk_constraint.get('constrained_columns', [])

        # 2. 全ての列情報を取得
        columns_info = inspector.get_columns(table_name)

        # 3. 主キー列名リストに含まれない列名だけをフィルタリングして抽出
        non_pk_column_names = [
            col['name']
            for col in columns_info
            if col['name'] not in pk_column_names
        ]

        return non_pk_column_names

        # columns_info = inspector.get_columns(table_name)
        # column_names = [col['name'] for col in columns_info]

        # return column_names

    @classmethod
    def get_all_db(cls):
        with session_scope() as session:
            results = session.query(cls).all()
            # return self.to_dict(self, results)
            return [
                {c.name: getattr(result, c.name) for c in cls.__table__.columns}
                for result in results
            ]

    @classmethod
    def get_result_view_all(cls, page, *args, **kwargs):
        # query = select(
        #     Decedent.code,
        #     # Decedent.responsible_person.label("担当者"),
        #     Decedent.situation.label("状況"),
        #     Decedent.folder_path.label("フォルダ"),
        #     func.concat(Decedent.username1, "  ", Decedent.username2).label("被相続人"),
        #     # func.concat(Heir.username1, "  ", Heir.username2).label("依頼人"),
        #     # Heir.updated_date.label("更新日"),
        #     # Heir.note.label("内容"),
        #     # Heir.contact_home.label("自宅電話番号"),
        #     # Heir.contact_phone.label("携帯電話番号"),
        #     Decedent.note.label("備考"),
        # )

        select_list = [
            Decedent.code,
            # Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_path.label("フォルダ"),
            func.concat(Decedent.username1, "  ", Decedent.username2).label("被相続人"),
            Column("　").label("依頼人"),  # column関数を使って存在しない列を表現
            Column("　").label("更新日"),
            Column("　").label("内容"),
            Column("　").label("自宅電話番号"),
            Column("　").label("携帯電話番号"),
            Decedent.note.label("備考"),
        ]

        query = select(*select_list)
        print("hasattr(cls, 'Heir'):")

        if hasattr(cls, 'Heir') and hasattr(cls.Heir, 'code'):
            # select_list = list(query.columns)
            # select_list.extend([
            #     func.concat(cls.Heir.username1, "  ", cls.Heir.username2).label("依頼人"),
            #     cls.Heir.updated_date.label("更新日"),
            #     cls.Heir.note.label("内容"),
            #     cls.Heir.contact_home.label("自宅電話番号"),
            #     cls.Heir.contact_phone.label("携帯電話番号"),
            # ])
            select_list = [
                cls.Decedent.code,
                # cls.Decedent.responsible_person.label("担当者"),
                cls.Decedent.situation.label("状況"),
                cls.Decedent.folder_path.label("フォルダ"),
                func.concat(cls.Decedent.username1, "  ", cls.Decedent.username2).label("被相続人"),
                # Heir関連の列が存在するため、実際の列に置き換え
                func.concat(cls.Heir.username1, "  ", cls.Heir.username2).label("依頼人"),
                cls.Heir.updated_date.label("更新日"),
                cls.Heir.note.label("内容"),
                cls.Heir.contact_home.label("自宅電話番号"),
                cls.Heir.contact_phone.label("携帯電話番号"),
                cls.Decedent.note.label("備考"),
            ]

            # 新しいSELECTリストでクエリを再構成
            query = select(*select_list)

            # LEFT OUTER JOINを実行
            query = query.outerjoin(cls.Heir, cls.Heir.code == cls.Decedent.code)

            # query = select(*select_list)
            # query = query.join(cls.Heir, cls.Heir.code == cls.Decedent.code)

        # query = query.join(Heir, Heir.code == Decedent.code)

        # query = query.where(Heir.offer == 1)
        # if page.session.get("/home").ch_contractor.value:
        #     query = query.where(
        #         and_(
        #             Decedent.situation != "手続終了",
        #             Decedent.situation != "キャンセル",
        #             Decedent.situation != "",
        #         )
        #     )
        # if 'me_rep_person' in kwargs:
        # if page.session.get('/home').ch_me_rep_person.value:
        #     query = query.where(Decedent.responsible_person == '森町')
        # query = query.where(Decedent.responsible_person == kwargs['me_rep_person'])

        # query = query.order_by(Heir.updated_date.asc())
        # query = query.order_by(Decedent.code.asc())
        print()
        print('query:', query)
        print()
        with session_scope() as session:
            results = session.execute(query).mappings().all()
            return results


class Decedent(BaseModel):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    code = Column(String)
    username1 = Column(String)
    username2 = Column(String)
    username1_hurigana = Column(String)
    username2_hurigana = Column(String)
    birthday = Column(String)
    deathday = Column(String)
    domicile = Column(String)
    zipcode = Column(String)
    prefectures = Column(String)
    municipalities = Column(String)
    townarea = Column(String)
    house_number = Column(String)
    building = Column(String)
    will = Column(CHAR)
    folder_path = Column(String)
    # maiden_name = Column(String)
    old_address1 = Column(String)
    old_address2 = Column(String)
    old_address3 = Column(String)
    # maiden_name_huri = Column(String)
    situation = Column(String)
    note = Column(String)
    responsible_person = Column(String)

    def __repr__(self):
        return f'code:{self.code} name:{self.username1} {self.username2}'
    
    @classmethod
    def get_customer(cls, page, *args, **kwargs):
        query = select(
            Decedent.code,
            # Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_path.label("フォルダ"),
            func.concat(Decedent.username1, "  ", Decedent.username2).label("被相続人"),
            func.concat(Heir.username1, "  ", Heir.username2).label("依頼人"),
            Heir.contact_home.label("自宅電話番号"),
            Heir.contact_phone.label("携帯電話番号"),
            Heir.updated_date.label("更新日"),
            Heir.note.label("内容"),
            Decedent.note.label("備考"),
        )
        query = query.join(Heir, Heir.code == Decedent.code)
        # query = query.where(Heir.offer == 1)
        # if 'me_rep_person' in kwargs:

        # # 自分の担当者
        # if page.session.get("/home").ch_me_rep_person.value:
        #     query = query.where(Decedent.responsible_person == "森町")

        # 手続き中
        if page.session.get("/home").ch_contractor.value:
            query = query.where(
                and_(
                    Decedent.situation != "手続終了",
                    Decedent.situation != "キャンセル",
                    Decedent.situation != "",
                )
            )

        if "dict" in kwargs:
            for key, value in kwargs["dict"].items():
                if key == "被相続人：姓かな":
                    query = query.where(cls.username1_hurigana.like(f"{value}%"))
                if key == "被相続人：姓":
                    query = query.where(cls.username1.like(f"%{value}%"))
                # if key == "担当者":
                #     query = query.where(cls.responsible_person == value)
                if key == "状況":
                    query = query.where(cls.situation == value)
                if key == "備考":
                    query = query.where(cls.note.like(f"%{value}%"))

        query = query.order_by(Heir.updated_date.asc())
        # query = query.order_by(Decedent.code.asc())
        with session_scope() as session:
            results = session.execute(query).mappings().all()
            return results

    @classmethod
    def delete_all(cls):
        with session_scope() as session:
            stmt = delete(cls)
            print('stmt:', stmt)
            session.execute(stmt)


class Heir(BaseModel):
    __tablename__ = "heir"
    heir_id = Column(Integer, primary_key=True)
    code = Column(String)
    username1 = Column(String)
    username2 = Column(String)
    username1_hurigana = Column(String)
    username2_hurigana = Column(String)
    contact_home = Column(String)
    contact_phone = Column(String)
    birthday = Column(Date)
    deathday = Column(Date)
    relationship = Column(String)
    relationship2 = Column(String)
    situation = Column(String)
    zipcode = Column(String)
    prefectures = Column(String)
    municipalities = Column(String)
    townarea = Column(String)
    house_number = Column(String)
    building = Column(String)
    offer = Column(Integer)
    transfer = Column(Integer)
    legal_heir = Column(Integer)
    Inheritance_form = Column(String)
    mail = Column(String)
    note = Column(String)
    updated_date = Column(String)

    @classmethod
    def get_customer(cls, page, *args, **kwargs):
        query = select(
            Decedent.code,
            Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_path.label("フォルダ"),
            func.concat(Decedent.username1, "  ", Decedent.username2).label("被相続人"),
            func.concat(Heir.username1, "  ", Heir.username2).label("依頼人"),
            Heir.contact_home.label("自宅電話番号"),
            Heir.contact_phone.label("携帯電話番号"),
            Heir.updated_date.label("更新日"),
            Heir.note.label("内容"),
            Decedent.note.label("備考"),
        )
        query = query.join(Heir, Heir.code == Decedent.code)
        query = query.where(Heir.offer == 1)
        query = query.order_by(Heir.updated_date.asc())
        # if page.session.get("/home").ch_me_rep_person.value:
        #     query = query.where(Decedent.responsible_person == "森町")
        if page.session.get("/home").ch_contractor.value:
            query = query.where(
                and_(
                    Decedent.situation != "手続終了",
                    Decedent.situation != "キャンセル",
                    Decedent.situation != "",
                )
            )
        if "dict" in kwargs:
            # for key, value in dict.items():
            for key, value in kwargs["dict"].items():
                if key == "依頼人：姓かな":
                    query = query.where(cls.username1_hurigana.like(f"{value}%"))
                if key == "依頼人：姓":
                    query = query.where(cls.username1.like(f"%{value}%"))
                if key == "電話番号":
                    query = query.filter(
                        or_(
                            cls.contact_home.like(f"%{value}%"),
                            cls.contact_phone.like(f"%{value}%"),
                        )
                    )

        with session_scope() as session:
            results = session.execute(query).mappings().all()
            return results

    @classmethod
    def delete_all(cls):
        with session_scope() as session:
            stmt = delete(cls)
            session.execute(stmt)


class Staff(BaseModel):
    __tablename__ = "staff"
    staff_id = Column(Integer, primary_key=True)
    name1 = Column(String)
    name2 = Column(String)
    name1_huri = Column(String)
    name2_huri = Column(String)
    counseling = Column(Integer)
    responsible_person = Column(Integer)
    tax_rep_person = Column(Integer)
    general_affairs_rep_person = Column(Integer)
    mail = Column(String)
    tel = Column(String)

    @classmethod
    def get_all_staff(cls):
        with session_scope() as session:
            results = session.query(cls).all()
            return [
                {c.name: getattr(result, c.name) for c in cls.__table__.columns}
                for result in results
            ]

    @classmethod
    def upsert(cls, *args, **kwargs):
        # stmt = update(Staff)
        # for arg in args[0]:
        #     if arg.__class__.__name__ == 'CustomTextField':
        #         print('arg:', arg.value)
        #         stmt = stmt.values(f'{arg.hint_text}={arg.value}')

        new_users = [
            {"staff_id": 1, "name1": "Alice", "mail": "alice@example.com"},
            {"staff_id": 2, "name1": "Bob", "mail": "bob@example.com"},
        ]

        with session_scope() as session:
            for data in new_users:
                user = session.merge(Staff(**data))
                session.add(user)
        #     existing_id = session.query(self).filter_by(email=self.staff_id).first()
        #     session.merge(stmt)

    @classmethod
    def delete(cls, data):
        with session_scope() as session:
            user_to_delete = session.query(Staff).filter_by(staff_id=data).first()
            session.delete(user_to_delete)


class ResponsiblePerson(BaseModel):
    __tablename__ = "responsible_person"
    responsible_person_id = Column(Integer, primary_key=True)
    name1 = Column(String)
    name2 = Column(String)
    name1_huri = Column(String)
    name2_huri = Column(String)

    @classmethod
    def get_responsible_person(cls):
        with session_scope() as session:
            results = session.query(cls).all()
            return BaseModel.to_dict(cls, results)

    @classmethod
    def get_responsible_person_dropdown(cls):
        with session_scope() as session:
            query = select(cls.name1)
            result = session.execute(query).mappings().all()
            return result


class TaxRepPerson(BaseModel):
    __tablename__ = "tax_rep_person"
    tax_rep_person_id = Column(Integer, primary_key=True)
    name1 = Column(String)
    name2 = Column(String)
    name1_huri = Column(String)
    name2_huri = Column(String)

    @classmethod
    def get_tax_rep_person_dropdown(cls):
        with session_scope() as session:
            query = select(cls.name1)
            result = session.execute(query).mappings().all()
            return result


def main():
    print('models起動')
    # print(Decedent.get_table_columns_info('customer'))
    # Decedent.recreate_all_tables()
    print()
    print(Decedent.get_all_db())
    print()
    print(Heir.get_all_db())


if __name__ == "__main__":
    main()
