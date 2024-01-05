from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqldb://clement:4141Clement?@localhost:3306/backendzone',
            pool_pre_ping=True,
            echo=True
        )
        self.reload()

    def all(self, cls):
        obj_list = []
        for obj in self.__session.scalars(select(cls)).all():
            obj_list.append(obj)
        return obj_list

    def check_if_exists(self, cls, **kwargs):
        for obj in self.__session.scalars(select(cls).filter_by(**kwargs)).all():
            return obj
        return False

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        from ..basemodel import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session()

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()