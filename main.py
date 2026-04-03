import datetime

from flask import Flask, request, render_template, make_response, session, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import data.jobs
from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "legdphb40wbpkwgphobdslzkpPKOVpvkeowjvbe20jasjOPJPJOvjovpbJOPBopwv"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
# app.register_blueprint(blueprint)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def main():
    return redirect("/login")


@app.route("/abc")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    # app.run(host="127.0.0.1", port=8081, debug=True)

    user1 = User()
    user1.surname = "Scott"
    user1.name = "Ridley"
    user1.age = "21"
    user1.position = "captain"
    user1.speciality = "research engineer"
    user1.address = "module_1"
    user1.email = "scott_chief@mars.org"
    db_sess.add(user1)

    user2 = User()
    user2.surname = "Mac"
    user2.name = "Demarco"
    user2.age = "35"
    user2.position = "colonist"
    user2.speciality = "pilot"
    user2.address = "module_2"
    user2.email = "mac@mars.org"
    db_sess.add(user2)

    user3 = User()
    user3.surname = "Def"
    user3.name = "Forinrange"
    user3.age = "14"
    user3.position = "colonist"
    user3.speciality = "builder"
    user3.address = "module_3"
    user3.email = "Else@mars.org"
    db_sess.add(user3)

    user4 = User()
    user4.surname = "Man"
    user4.name = "Normal"
    user4.age = "88"
    user4.position = "colonist"
    user4.speciality = "Normal Worker"
    user4.address = "module_4"
    user4.email = "Absolutely_normal_man@mars.org"
    db_sess.add(user4)

    job1 = data.jobs.Jobs()
    job1.team_leader = 1
    job1.job = "deployment of residential modules 1 and 2"
    job1.work_size = 15
    job1.collaborators = "2, 3"
    job1.start_date = datetime.datetime.now()
    job1.is_finished = False
    db_sess.commit()

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         print(form.username.data)
#     return render_template("login.html", title="вход", form=form)
