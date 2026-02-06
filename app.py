from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pro_secret_key_99'

raw_db_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url.replace("postgres://", "postgresql://", 1) if raw_db_url else 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'student_login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.String(50))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    content = db.Column(db.Text)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(10))
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    input_format = db.Column(db.String(100))
    constraints = db.Column(db.String(100))
    output_format = db.Column(db.String(100))
    sample_input = db.Column(db.String(100))
    sample_output = db.Column(db.String(100))
    explanation = db.Column(db.Text)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='arun').first():
        db.session.add(User(username='arun', password='arun123'))
        db.session.commit()

@app.route('/')
def home():
    return render_template('start_page.html')

@app.route('/student_new')
def student() :
    events = Event.query.all()
    return render_template('student_question_view.html', events=events)

@app.route('/student_login',methods = ['GET' , 'POST'])
def student_login() :
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('student_problem_view'))
        flash('Invalid Credentials')
    return render_template('student_login.html')

@app.route('/student_problem_view')
@login_required
def student_problem_view() :
    events = Event.query.all()
    return render_template("student_problem_view.html", events=events)



@app.route('/student_profile')
def student_profile ():
    return render_template('student_profile.html')

@app.route('/admin/question_add',methods=['GET','POST'])
def admin_question_add() :
    if request.method=='POST' :
        new_q = Question(
        question_id = request.form.get('question_id'),
        title=request.form.get('title'),
        description=request.form.get('description'),
        input_format = request.form.get('input_format'),
        constraints=request.form.get('constraints'),
        output_format = request.form.get('output_format'),
        sample_input = request.form.get('sample_input'),
        sample_output = request.form.get('sample_output'),
        explanation = request.form.get('explanation')
    )
        db.session.add(new_q)
        db.session.commit()
        flash('Question published successfully!')
        return redirect(url_for('admin_panel'))
    return redirect(url_for('admin_panel'))
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('admin_panel'))
        flash('Invalid Credentials')
    return render_template('admin_login.html')

@app.route('/admin')
@login_required
def admin_panel():
    events = Event.query.all()
    messages = Message.query.all()
    questions = Question.query.all()
    return render_template('admin.html', events=events, messages=messages, questions=questions)

@app.route('/admin/add_event', methods=['POST'])
@login_required
def add_event():
    db.session.add(Event(
        title=request.form.get('title'),
        date=request.form.get('date'),
        location=request.form.get('location'),
        description=request.form.get('description')
    ))
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.date = request.form.get('date')
        event.location = request.form.get('location')
        event.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin_panel'))
    return render_template('updated.html', event=event)

@app.route('/admin/delete_event/<int:id>')
@login_required
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_msg/<int:id>')
@login_required
def delete_msg(id):
    db.session.delete(Message.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)