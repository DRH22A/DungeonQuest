from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_bcrypt import Bcrypt
from models import db, User  # Import User model from models.py
import webbrowser
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
db.init_app(app)
bcrypt = Bcrypt(app)

# Define the sign-up form
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Player', 'Player'), ('Spectator', 'Spectator'), ('Admin', 'Admin')])
    submit = SubmitField('Sign Up')

# Define the sign-in form
class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Define the sign-up route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        # Process the form data and create the user account
        username = form.username.data
        password = form.password.data
        role = form.role.data
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('sign_up.html', form=form, error='Username already exists.')

        # Create a new user object
        new_user = User(username=username, password=password, role=role)
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the confirmation page after successful sign-up
        return redirect('/confirmation')
    return render_template('sign_up.html', form=form)

# Define the sign-in route
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        # Process the form data and authenticate the user
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # User exists and password is correct
            return redirect('/')  # Redirect to the home page or any other page
        else:
            # Invalid username or password
            error = 'Invalid username or password'
            return render_template('sign_in.html', form=form, error=error)
    return render_template('sign_in.html', form=form)

# Define the confirmation route
@app.route('/confirmation')
def confirmation():
    # Retrieve the username and role of the last signed-up user from the database
    last_user = User.query.order_by(User.id.desc()).first()
    if last_user:
        username = last_user.username
        role = last_user.role
    else:
        # If no user found, provide default values
        username = "Unknown"
        role = "Unknown"
    
    # Render the confirmation page with username and role
    return render_template('confirmation_of_sign_up.html', username=username, role=role)

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()
        
        # Open the sign-up page in the default web browser
        webbrowser.open_new("http://localhost:5000/sign_up")
        
        # Run the Flask app
        app.run(debug=True)
