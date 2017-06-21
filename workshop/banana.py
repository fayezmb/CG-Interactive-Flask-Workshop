from flask import Flask, render_template, request
from flask_mail import Message
from flask_mail import Mail
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import *

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'workshopflask@gmail.com'
app.config['MAIL_PASSWORD'] = 'flaskworkshop34'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)
mail = Mail(app)


# class User(db.Model):  # DB table / User class
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):  # sqlalchemy initialization method
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username
roles_users = db.Table('roles_users',db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, 	backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Wahabu@localhost/postgres'


# postgresql://user:password@localhost
@app.route('/')
def x():
    return "welcome to your first page"


@app.route('/page2')
@login_required
def y():
    return "welcome to page 2"


@app.route('/page3')
def z():
    return render_template("sample.html")


@app.route('/page4/<name2>')
def a(name2):
    return render_template("name.html", name=name2)


@app.route('/page5')
def b():
    return render_template("formsample.html")


@app.route('/page6', methods=['POST'])
def c():
    y = request.form['username']
    print y
    return (request.form['email'], request.form['username'])


@app.route('/page7', methods=['POST', 'GET'])
def d():
    if request.method == 'GET':
        # show html form
        return '''
             <form method="post">
                 <input type="text" name="expression" />
                 <input type="submit" value="Calculate" />
             </form>
         '''
    elif request.method == 'POST':
        # calculate result
        expression = request.form['expression']
        result = eval(expression)
        return 'result: %s' % result


@app.route('/page8')
def index():
    for x in range(0, 5):
        msg = Message('Is this the subject?', sender='workshopflask@gmail.com',
                      recipients=['abdulwahab@cg-interactive.com'])
        msg.body = "Hello Flask message sent from Flask-Mail %d" % x
        mail.send(msg)
    return "Sent"
@app.route('/page9')
def page1():
   return render_template("add_user.html")

@app.route('/post_user', methods=['POST'])
def post_user():
   user = User(request.form['username'], request.form['email'])
   db.session.add(user)
   db.session.commit()
   return redirect(url_for('user', name=user.username))
@app.route("/user/<name>")
def user(name):
   user = User.query.filter_by(username=name).first()
   return render_template("profile.html", user=user)
app.debug = True
db.create_all()
db.session.commit()
if __name__ == "__main__":
    app.run(debug=True)
