from sqlalchemy import CHAR, Column, Date, Integer, String, and_, func, or_, select

from . import Base, session_scope


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self, results):
        return [
            {c.name: getattr(result, c.name) for c in self.__table__.columns}
            for result in results
        ]

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
        query = select(
            Decedent.code,
            # Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_s_path.label("フォルダ"),
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
        if page.session.get("/home").ch_contractor.value:
            query = query.where(
                and_(
                    Decedent.situation != "手続終了",
                    Decedent.situation != "キャンセル",
                    Decedent.situation != "",
                )
            )
        # if 'me_rep_person' in kwargs:
        # if page.session.get('/home').ch_me_rep_person.value:
        #     query = query.where(Decedent.responsible_person == '森町')
        # query = query.where(Decedent.responsible_person == kwargs['me_rep_person'])
        query = query.order_by(Heir.updated_date.asc())
        # query = query.order_by(Decedent.code.asc())
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
    folder_s_path = Column(String)
    maiden_name = Column(String)
    old_address1 = Column(String)
    old_address2 = Column(String)
    old_address3 = Column(String)
    maiden_name_huri = Column(String)
    situation = Column(String)
    note = Column(String)
    responsible_person = Column(String)

    @classmethod
    def get_customer(cls, page, *args, **kwargs):
        query = select(
            Decedent.code,
            # Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_s_path.label("フォルダ"),
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
    # def get_customer(cls, dict):
    def get_customer(cls, page, *args, **kwargs):
        query = select(
            Decedent.code,
            Decedent.responsible_person.label("担当者"),
            Decedent.situation.label("状況"),
            Decedent.folder_s_path.label("フォルダ"),
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
        if page.session.get("/home").ch_me_rep_person.value:
            query = query.where(Decedent.responsible_person == "森町")
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
