from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from . import BaseModel, Base
from .email import Email
from .password import Password


class Profile(BaseModel, Base):
    __tablename__ = "profiles"
    user = relationship("User", back_populates="profile", uselist=False, cascade="save-update")

    profile_img_url = Column(String(250))
    dob = Column(DateTime, default=datetime.utcnow(), nullable=False)

    email_id = Column(String(60), ForeignKey("emails.id"), nullable=False)
    email = relationship("Email", uselist=False, back_populates="profile")
    phone_number = Column(String(60), nullable=False)

    password_id = Column(String(60), ForeignKey("passwords.id"), nullable=False)
    password = relationship("Password", uselist=False, back_populates="profile")

    def __init__(self, email: str, phone_number: str, password: str, profile_img_url: str, dob):
        super().__init__()

        tmp_email = Email(email)
        tmp_password = Password(password)

        self.email_id = tmp_email.id
        self.email = tmp_email
        self.phone_number = phone_number

        self.password_id = tmp_password.id
        self.password = tmp_password

        self.profile_img_url = profile_img_url
        self.dob = dob
