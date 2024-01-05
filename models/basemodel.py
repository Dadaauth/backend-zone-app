from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DATETIME
import uuid
from datetime import datetime

Base = declarative_base()


class BaseModel:
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow(),nullable=False)
    updated_at = Column(DATETIME, default=datetime.utcnow(), nullable=False)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @classmethod
    def all(cls):
        """Retrieves all instances of a model object from the database"""
        from .__init__ import storage
        return storage.all(cls)

    def check_if_exists(self, **kwargs):
        from .__init__ import storage
        return storage.check_if_exists(self.__class__, **kwargs)

    def to_dict(self):
        """Returns a dictionary representation of the model object"""
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        from .__init__ import storage
        storage.delete(self)
        storage.save()

    def save(self):
        from .__init__ import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()
