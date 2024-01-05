import os, time
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.utils import secure_filename

from ..models.user_related.user import User
from ..models.user_related.email import Email

app = Flask(__name__)
app.secret_key = 'fxiwdjvknbs,dsfe3762783cb37h8f'
CORS(app, ["http://localhost:3000"])
login_manager = LoginManager()
login_manager.init_app(app)
# img_s_dir = os.path.join("")
img_s_dir = 'static/images/'


@login_manager.user_loader
def load_user(user_id):
    user_obj = User().check_if_exists(id=user_id)
    return user_obj if user_obj else None


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        user_email = request.form['email']
        phone_number = request.form['phone_number']
        dob = request.form['dob']
        password = request.form['password']
        profile_img_file = request.files['profile_picture']

        if Email().check_if_exists(email=user_email):
            return "<h3>User Account Already Exists</h3>"

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=user_email,
            phone_number=phone_number,
            password=password,
            dob=dob,
            profile_img_file=profile_img_file,
            img_s_dir=img_s_dir,
            img_ext=os.path.splitext(secure_filename(profile_img_file.filename))[1].lower()
        )
        new_user.save()
        return redirect("login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        error = request.args.get('error')
        if not error:
            error = ''
        return render_template("login.html", error=error)
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        start_time = time.time()
        email_obj = Email().check_if_exists(email=user_email)
        end_time = time.time()
        print(f"gotten email, time: {end_time - start_time} seconds")
        if email_obj:
            print("email exists, checking password...")
            start_time = time.time()
            if email_obj.profile.password.verify_password(password=user_password):
                end_time = time.time()
                print(f"password checked, time: {end_time - start_time} seconds")
                # user verified, login!
                user = email_obj.profile.user
                login_user(user, remember=True)
                return redirect('/dashboard')
            else:
                # User password is incorrect
                return redirect(url_for("login", error="Incorrect Password"))
        return redirect(url_for("login", error="User doesn't exist"))
