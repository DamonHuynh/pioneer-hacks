from flask import Flask, render_template, redirect, url_for, request, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm   
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user,\
      logout_user

#use PythonAnywhere to deploy when done

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubinfo.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized(): 
    return redirect(url_for('login'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(100), unique = True, index = True)
    password_hash = db.Column(db.String(128), unique = False, index = True)
    
    def __repr__(self): 
        return '<User {}>'.format(self.username)
    
    def generate_password(self, password): 
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password): 
        return check_password_hash(self.password_hash, password)
    
member_event = db.Table('member_event', 
      db.Column('member_id', db.Integer, db.ForeignKey('member.id')), 
      db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
      )

class Member(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = False, index = True)
    student_id = db.Column(db.Integer, index = True, unique = False)
    hours = db.Column(db.Integer, index = True, unique = False)
    grade = db.Column(db.Integer, index = True, unique = False)
    email = db.Column(db.String(100), unique = False, index = True)
    events = db.relationship('Event', secondary = member_event, backref = 'members')

class Event(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = False, index = True)
    description = db.Column(db.String(250), unique = False, index = True)
    address = db.Column(db.String(250), unique = False, index = True)
    date = db.Column(db.String(40), unique = False, index = True)
    hours = db.Column(db.Integer, index = True, unique = False)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard(): 
    if request.method == 'POST': 
        if 'name' in request.form: 
            member = Member(name = request.form['name'], student_id = request.form['id'],
                             hours = request.form['hours'], grade = request.form['grade'], email = request.form['email'])
            try: 
                db.session.add(member)
                db.session.commit()
            except Exception as e: 
                print(e)
        elif request.form['eventName']: 
            event = Event(name = request.form['eventName'], description = request.form['description'],
                             date = request.form['date'], hours = request.form['hours'], address = request.form['address'])
            for member in Member.query.all(): 
                if member.name in request.form:
                    member.hours += int(event.hours)
                    event.members.append(member)
                    member.events.append(event)
                
                
            try: 
                db.session.add(event)
                db.session.commit()
            except Exception as e: 
                print(e)
    members = Member.query.all()
    return render_template('dashboard.html', members = members)

@app.route('/event/<int:id>')
def event(id): 
    event = Event.query.get(id)
    return render_template('event.html', event = event)

@app.route('/events')
def events(): 
    events = Event.query.all()
    return render_template('events.html', events = events)

@app.route('/member/<int:id>')
def member(id): 
    member = Member.query.get(id)
    return render_template('member.html', member = member)

@app.route('/members')
def members(): 
    members = Member.query.all()
    return render_template('members.html', members = members)

@app.route('/login', methods = ['GET', 'POST'])
def login(): 
    if request.method == 'POST': 
        user = User.query.filter_by(username = request.form['username']).first()
        if user == None or not user.check_password(request.form['password']):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')




