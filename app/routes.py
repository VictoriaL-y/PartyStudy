import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_marshmallow import fields

# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
from app import app, db, bcrypt, mail
from app.models import User, Party, UserSchema, PartySchema
from app.forms import (RegistrationForm, LoginForm, UpdateProfileForm,
                         PartyForm, RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# partys = [
#     {
#         'title': 'Python',
#         'host': 'VictoriaL-y',
#         'description': 'I would like to get together and create a python blog!',
#         'Date&Time': '18.02.2030, 18:00 - 21:00',
#         'address': 'Pariser Platz, 10117 Berlin',
#         'language': 'English',
#         "chat's Link": 'https://whatsapp.com/gGjfHe2r523'
#     },
#     {
#         'title': 'English',
#         'host': 'John-Doe',
#         'description': 'I would like to learn English together!',
#         'Date&Time': '02.03.2030, 17:00 - 20:00',
#         'address': 'Alexanderplatz, 10178 Berlin',
#         'anguage': 'English',
#         "chat's Link": 'https://whatsapp.com/Khbsf57HF3f'
#     }
# ]

@app.route("/")
@app.route("/welcome")
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    return render_template("index.html", title="Welcome to StudyParty!")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Now you are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('map'))
        else:
            flash('Login unsuccessful. Please check e-mail and password', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route("/profile")
@login_required
def profile():
    form = PartyForm()
    page = request.args.get('page_host', 1, type=int)
    parties = Party.query.filter(Party.author==current_user).order_by(Party.date_posted.desc()).paginate(page=page, per_page=2)
    page_2 = request.args.get('page_att', 1, type=int)
    parties_2 = Party.query.join(User.attending).filter(User.id == current_user.id).order_by(Party.date_posted.desc()).paginate(page=page_2, per_page=2)
    image_avatar_file = url_for('static', filename='profile_pics/' + current_user.image_avatar_file)
    image_bg_file = url_for('static', filename='profile_pics/' + current_user.image_bg_file)
    return render_template("profile.html", title="Profile", image_avatar_file=image_avatar_file, image_bg_file=image_bg_file, parties=parties, parties_2=parties_2, form=form)

def save_avatar_picture(form_avatar_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_avatar_picture.filename)
    picture_avatar_fn = random_hex + f_ext
    picture_avatar_path = os.path.join(app.root_path, 'static/profile_pics', picture_avatar_fn)
    

    output_size = (225, 225)
    i = Image.open(form_avatar_picture)
    i.thumbnail(output_size)
    i.save(picture_avatar_path)

    return picture_avatar_fn


def save_bg_picture(form_bg_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_bg_picture.filename)
    picture_bg_fn = random_hex + f_ext
    picture_bg_path = os.path.join(app.root_path, 'static/profile_pics', picture_bg_fn)
    

    output_size = (850, 850)
    i = Image.open(form_bg_picture)
    i.thumbnail(output_size)
    i.save(picture_bg_path)

    return picture_bg_fn

@app.route("/profile/update", methods=['GET', 'POST'])
@login_required
def updateProfile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.avatar_picture.data:
            avatar_file = save_avatar_picture(form.avatar_picture.data)
            current_user.image_avatar_file = avatar_file
        if form.bg_picture.data:
            bg_file = save_bg_picture(form.bg_picture.data)
            current_user.image_bg_file = bg_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.phoneNumber = form.phoneNumber.data
        current_user.location = form.location.data
        current_user.languages = form.languages.data
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.phoneNumber.data = current_user.phoneNumber
        form.location.data = current_user.location
        form.languages.data = current_user.languages
    image_avatar_file = url_for('static', filename='profile_pics/' + current_user.image_avatar_file)
    image_bg_file = url_for('static', filename='profile_pics/' + current_user.image_bg_file)
    return render_template("updateProfile.html", title="Updating profile", image_avatar_file=image_avatar_file, image_bg_file=image_bg_file, form=form)

@app.route("/party/new", methods=['GET', 'POST'])
@login_required
def new_party():
    form = PartyForm()
    if form.validate_on_submit():
        party = Party(title=form.title.data, date_time=form.date_time.data, address=form.address.data, lat=form.lat.data, lng=form.lng.data, whatsapp_link=form.whatsapp_link.data, 
                    party_languages=form.party_languages.data, description=form.description.data, author=current_user)
        db.session.add(party)
        db.session.commit()
        flash('Your party has been created!', 'success')
        return redirect(url_for('profile'))
    image_avatar_file = url_for('static', filename='profile_pics/' + current_user.image_avatar_file)
    image_bg_file = url_for('static', filename='profile_pics/' + current_user.image_bg_file)
    return render_template("create_party.html", title='New Party', image_avatar_file=image_avatar_file, image_bg_file=image_bg_file, form=form, legend='New Party')

@app.route("/party/<int:party_id>")
def party(party_id):
    form = PartyForm()
    party = Party.query.get_or_404(party_id)
    image_avatar_file = url_for('static', filename='profile_pics/' + current_user.image_avatar_file)
    image_bg_file = url_for('static', filename='profile_pics/' + current_user.image_bg_file)
    return render_template('party.html', title=party.title, image_avatar_file=image_avatar_file, image_bg_file=image_bg_file, party=party, form=form)

@app.route("/party/<int:party_id>/update", methods=['GET', 'POST'])
@login_required
def update_party(party_id):
    party = Party.query.get_or_404(party_id)
    if party.author != current_user:
        abort(403)
    form = PartyForm()
    if form.validate_on_submit():
        party.title = form.title.data
        party.date_time = form.date_time.data
        party.address = form.address.data
        party.lat = form.lat.data
        party.lng = form.lng.data
        party.whatsapp_link = form.whatsapp_link.data
        party.party_languages = form.party_languages.data
        party.description = form.description.data
        db.session.commit()
        flash('Your party has been updated!', 'success')
        return redirect(url_for('party', party_id=party.id))
    elif request.method == 'GET':
        form.title.data = party.title
        form.date_time.data = party.date_time
        form.address.data = party.address
        form.lat.data = party.lat
        form.lng.data = party.lng
        form.whatsapp_link.data = party.whatsapp_link
        form.party_languages.data = party.party_languages
        form.description.data = party.description
    image_avatar_file = url_for('static', filename='profile_pics/' + current_user.image_avatar_file)
    image_bg_file = url_for('static', filename='profile_pics/' + current_user.image_bg_file)
    return render_template("create_party.html", title='Update Party', image_avatar_file=image_avatar_file, 
                            image_bg_file=image_bg_file, form=form, legend='Update Party')

@app.route("/party/<int:party_id>/delete", methods=['POST'])
@login_required
def delete_party(party_id):
    party = Party.query.get_or_404(party_id)
    if party.author != current_user:
        abort(403)
    db.session.delete(party)
    db.session.commit()
    flash('Your party has been deleted!', 'success')
    return redirect(url_for('profile'))

@app.route("/map")
def map():
    form = PartyForm()
    parties = Party.query.order_by(Party.date_posted.desc())
    return render_template("map.html", form=form, parties=parties)

@app.route("/map/attending/<int:party_id>", methods=['GET', 'POST'])
@login_required
def appendUser(party_id):
    party = Party.query.get_or_404(party_id)
    current_user.attending.append(party)
    db.session.commit()
    flash('Your have joined the party!', 'success')
    return redirect(url_for('map'))

@app.route("/map/leave/<int:party_id>", methods=['GET', 'POST'])
@login_required
def leaveTroughMap(party_id):
    party = Party.query.get_or_404(party_id)
    current_user.attending.remove(party)
    db.session.commit()
    flash('Your have left the party!', 'danger')
    return redirect(url_for('map'))

@app.route("/profile/leave/<int:party_id>", methods=['GET', 'POST'])
@login_required
def leaveTroughProfile(party_id):
    party = Party.query.get_or_404(party_id)
    current_user.attending.remove(party)
    db.session.commit()
    flash('Your have left the party!', 'danger')
    return redirect(url_for('profile'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.html = render_template('email/reset_password.html',
                                         user=user, token=token)
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/api")
def api():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    return jsonify({'user' : output})