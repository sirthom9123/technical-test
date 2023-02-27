from ..app import db, app
from ..forms import Form
from flask import render_template

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    JSON
)
from sqlalchemy.orm import relationship
from flask_security import UserMixin, RoleMixin, Security, SQLAlchemyUserDatastore
from flask_security import LoginForm as Form
from flask_security import RegisterForm
from wtforms.fields.html5 import EmailField
from wtforms import StringField, PasswordField, validators, TextField
from wtforms.validators import DataRequired, Length, InputRequired, Required
from wtforms.widgets import TextArea


class User(db.Model, UserMixin):
    """
    A user who can login and use SCODA.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100))
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

    first_name = Column(String(50))
    last_name = Column(String(50))

    tours = Column(Boolean(), default=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    # associations
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User phone=%s>" % (self.phone,)

    # Flask-Security requires an active attribute
    @property
    def active(self):
        return not self.disabled

    @active.setter
    def active(self, value):
        self.disabled = not value

    @classmethod
    def create_defaults(self):
        from flask_security.utils import encrypt_password

        admin_user = User()
        admin_user.admin = True
        admin_user.email = "matthew@opendata.durban"
        admin_user.password = encrypt_password('admin')
        return [admin_user]


class Role(db.Model, RoleMixin):
    """
    Determines which features users can access.
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def create_defaults(self):
        return [
            Role(name='city', description='user can access city user panels'),
            Role(name='researcher', description='user can access researcher panel')
        ]


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE')))


class LoginForm(Form):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class EmailForm(Form):
    description = StringField('Comment', [validators.DataRequired()], widget=TextArea())

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

    def validate(self):
        return super(EmailForm, self).validate()

    def populate_obj(self, obj):
        super(EmailForm, self).populate_obj(obj)


# user authentication
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
