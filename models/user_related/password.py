from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
import bcrypt
from . import BaseModel, Base


class Password(BaseModel, Base):
    __tablename__ = 'passwords'
    profile = relationship("Profile", uselist=False, back_populates="password")
    password = Column(String(250), nullable=False)

    def __init__(self, password: str) -> None:
        super().__init__()
        self.password = password
        self.hash_password()

    def hash_password(self):
        # Note that bcrypt can only handle a maximum of 72 characters
        # TODO: There is a workaround, check the bcrypt docs on pypi.org
        self.password = bcrypt.hashpw(bytes(self.password, 'utf-8'), bcrypt.gensalt(rounds=15))

    def verify_password(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password, 'utf-8'))

