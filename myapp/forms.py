from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TelField, BooleanField, EmailField, PasswordField, ValidationError
from wtforms.validators import InputRequired, DataRequired, Length, Email, Regexp
from databases import User

class QuantityForm(FlaskForm):
    quantity = SelectField("", choices=[(i, str(i)) for i in range(1, 11)], validators=[InputRequired()])
    submit = SubmitField("Add to basket")

class RemoveFromBasketForm(FlaskForm):
    submit = SubmitField('X')

class EditAddressForm(FlaskForm):
    submit = SubmitField('Use another address')
    form_id = 'edit_address'

class EditPaymentDetailsForm(FlaskForm):
    submit = SubmitField('Use another payment method')
    form_id = 'edit_payment'
    
class SearchForm(FlaskForm):
    search = StringField('')

class AddressForm(FlaskForm):
    full_name = StringField('Full name', [InputRequired(), Length(max=100)], render_kw={'placeholder': 'John Doe'})
    phone_number = TelField('Phone number', [InputRequired()], render_kw={'placeholder': '07400 456 789'})
    postcode = StringField('Postcode', [InputRequired(), Length(max=7)], render_kw={'placeholder': 'Enter your area postcode'})
    address_line_one = StringField('Address line 1', [InputRequired(), Length(max=100)])
    address_line_two = StringField('Address line 2', [InputRequired(), Length(max=100)])
    town_city = StringField('Town / City', [InputRequired(), Length(max=100)])
    county = StringField('County (if applicable)', [Length(max=100)])
    submit = SubmitField('Use this address')
    
class PaymentForm(FlaskForm):
    name_on_card = StringField('Name on card', [InputRequired(), Regexp(r'^[a-zA-Z\s\'\.-]+$', message="Only letters, spaces, apostrophes, periods, or hyphens")])
    card_number = StringField('Card number', [InputRequired(), Length(max=19), Regexp(r'^[0-9\s-]*$', message="Only numbers, hyphens, or spaces")])
    expiry_date = StringField('Expiry date (MMYY)', [InputRequired(), Length(max=4, min=4, message="Enter in format MMYY"), Regexp(r'^[0-9]*$')])
    security_number = StringField('Security pin', [InputRequired(), Length(max=3, min=3), Regexp(r'^[0-9]*$')])
    submit = SubmitField('Use this payment method')
    
    def validate_card_number(self, card_number):
        isIncorrectFormat = False
        existing_card_number = str(card_number.data).replace('-', '').replace(' ', '')
        if len(existing_card_number) < 16:
            isIncorrectFormat = True
        if '-' in card_number.data and ' ' in card_number.data:
            isIncorrectFormat = True
        if isIncorrectFormat:
            raise ValidationError("Incorrect format. Try again.")

class RegistrationForm(FlaskForm):
    email = EmailField('Email', [InputRequired()], render_kw={'placeholder': 'user@example.com'})
    password = PasswordField('Password', [InputRequired(), Length(max=30, min=8)], render_kw={'placeholder': 'password'})
    reenter_password = PasswordField('Re-enter password', [InputRequired(), Length(max=30, min=8)], render_kw={'placeholder': 'password'})
    username = StringField('Username', [InputRequired(), Length(max=30, min=8), Regexp(r'^\w+$', message="Only letters, numbers, or underscores")], render_kw={'placeholder': 'exampleuser123'})
    submit = SubmitField('Create your account')
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        
        if existing_user_username:
            raise ValidationError("Username is taken.")
        
    def validate_password(self, password):
        chosen_password = password.data
        reentered_password = self.reenter_password.data
        
        if chosen_password != reentered_password:
            raise ValidationError("Passwords do not match.")
    
    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        
        if existing_user_email:
            raise ValidationError("Email is already in use.")
    
class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(max=30)], render_kw={'placeholder': 'exampleuser123'})
    password = PasswordField('Password', [InputRequired(), Length(max=30, min=8)], render_kw={'placeholder': 'password'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')