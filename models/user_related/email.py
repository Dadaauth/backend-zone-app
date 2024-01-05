from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import BaseModel, Base
from .password import Password


class Email(BaseModel, Base):
    __tablename__ = 'emails'
    profile = relationship("Profile", uselist=False, back_populates="email")
    email = Column(String(150), nullable=False)

    def __init__(self, email: str = None) -> None:
        super().__init__()
        if self.validate_email(email):
            self.email = email

    def validate_email(self, email):
        # validate user email addresses this may include sending
        # validation link to their email addresses
        return True
