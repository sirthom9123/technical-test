from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    func
    )
from wtforms import StringField,BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
import logging
from flask_security import UserMixin, RoleMixin,RegisterForm
from ..app import db, app
from wtforms import validators, PasswordField
from wtforms.fields.html5 import EmailField
from ..forms import Form

log = logging.getLogger(__name__)
from sqlalchemy.orm import column_property

class User(db.Model, UserMixin):
    """
    A user who can login and work with middleware.
    """
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True)
    email           = Column(String(50), index=True, nullable=False, unique=True)
    firstname       = Column(String(50), nullable=True)
    lastname        = Column(String(50), nullable=True)
    fullname        = column_property(firstname + " " + lastname)
    user_name       = Column(String(50), nullable=True)
    description     = Column(String(150),nullable=True)
    image           = Column(String, nullable=True)
    admin           = Column(Boolean, default=False)
    disabled        = Column(Boolean, default=False)
    password        = Column(String(100), default='')
    created_at      = Column(DateTime(timezone=True), index=True, unique=False, nullable=False, server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    roles           = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    verified        = Column(Boolean, default=False)


    def __repr__(self):
        return "<User email=%s>" % (self.email,)

    # Flask-Security requires an active attribute
    @property
    def active(self):
        return not self.disabled

    @active.setter
    def active(self, value):
        self.disabled = not value

    @classmethod
    def create_defaults(self):
        from flask_security.utils import hash_password

        admin_user = User()
        admin_user.first_name = "middleware"
        admin_user.last_name = "Admin"
        admin_user.user_name = "Admin"
        admin_user.admin = True
        admin_user.phone_number = ""
        admin_user.description = "Testing description"
        admin_user.email = "test@opendata.durban"
        admin_user.password = hash_password('admin@2019')

        return [admin_user]


class Role(db.Model, RoleMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return str(self.name)

    @classmethod
    def create_defaults(self):
        return [
                Role(name='user', description='user can use the standard features')
                ]


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE')))



class LoginForm(Form):
    email       = EmailField('Email', [validators.Required()])
    password    = PasswordField('Password', [validators.Required()])


# user authentication
from flask_security import Security, SQLAlchemyUserDatastore
from flask import render_template
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
app.extensions['security'].render_template = render_template

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number    = StringField('Phone Number', [validators.DataRequired(), Length(min=10, max=10)])
    newsletter = BooleanField([validators.Optional()],id="newsletterCheckbox")

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.newsletter.data = False

    def validate(self):
        return super(ExtendedRegisterForm, self).validate()

    def populate_obj(self, obj):
        super(ExtendedRegisterForm, self).populate_obj(obj)

class UserForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    # user_name      = StringField('Last Name', validators=[DataRequired(), Length(min=5, max=30)])
    description  = TextAreaField('Enter Description here', [validators.DataRequired(), Length(min=0,max=150)] )
    phone_number    = StringField('Phone Number', [validators.DataRequired(), Length(min=10, max=10)])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def validate(self):
        return super(UserForm, self).validate()

    def populate_obj(self, obj):
        super(UserForm, self).populate_obj(obj)
