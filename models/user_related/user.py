from sqlalchemy import Column, String, ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship
import uuid

from . import BaseModel, Base
from .profile import Profile


class User(BaseModel, Base, UserMixin):
    __tablename__ = 'users'

    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)

    profile_id = Column(String(60), ForeignKey("profiles.id"), nullable=False)
    profile = relationship(
        "Profile",
        uselist=False,
        back_populates="user",
        cascade="save-update",
        foreign_keys=profile_id
    )

    def __init__(self,
                 firstname=None,
                 lastname=None,
                 email=None,
                 phone_number=None,
                 password=None,
                 dob=None,
                 profile_img_file=None,
                 img_s_dir=None,
                 img_ext=None):
        super().__init__()
        if firstname is None or lastname is None or email is None or phone_number is None or password is None or dob is None or profile_img_file is None or img_s_dir is None or img_ext is None:
            return
        profile_img_url = f"{img_s_dir}{uuid.uuid4()}{img_ext}"
        self.firstname = firstname
        self.lastname = lastname
        profile_img_file.save(profile_img_url)

        tmp_profile = Profile(email, phone_number, password, profile_img_url, dob)
        self.profile_id = tmp_profile.id
        self.profile = tmp_profile
