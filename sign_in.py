from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt
from models import db, User
import webbrowser
import foundation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                # User exists and password is correct
                # Redirect to foundation.py
                # You need to know the URL where foundation.py is running
                # If it's running locally, it could be something like http://127.0.0.1:8000/
                # If you're unsure, check the configuration in foundation.py where the Flask app is being run (app.run())
                try:
                    foundation.MainGame([username, password])
                except:
                    print('DungeonQuest failed to launch!')

                return redirect('http://127.0.0.1:8000/')  # Adjust the URL as needed
            else:
                # Invalid username or password
                return render_template('sign_in.html', error='Invalid username or password')
        except KeyError:
            # Handle case when 'username' or 'password' field is missing in the form submission
            return render_template('sign_in.html', error='Username or password field is missing')
    else:
        # Handle GET request
        return render_template('sign_in.html')

if __name__ == '__main__':
    # Open the sign-in page in the default web browser before starting the Flask server
    webbrowser.open_new("http://127.0.0.1:8000/sign_in")
    
    # Start the Flask server
    app.run(host="127.0.0.1", port=8000)
