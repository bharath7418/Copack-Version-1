from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import db, login_manager
from .models import User, Message, Question
from .utils import execute_code

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def home():
    return render_template('start_page.html')

@bp.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('main.student_problem_view'))
        flash('Invalid Credentials')
    return render_template('student_login.html')

@bp.route('/student_problem_view')
@login_required
def student_problem_view():
    questions = Question.query.all()
    return render_template("student_problem_view.html", questions=questions)

@bp.route('/student_profile')
def student_profile():
    return render_template('student_profile.html')

@bp.route('/solve_and_compiler_page/<int:id>')
def solve_and_compiler_page(id):
    q = Question.query.get_or_404(id) 
    return render_template('solve_and_compiler_page.html', q=q)

@bp.route('/admin')
@login_required
def admin_panel():
    messages = Message.query.all()
    questions = Question.query.all()
    return render_template('admin.html', messages=messages, questions=questions)

@bp.route('/admin/question_add', methods=['GET', 'POST'])
def admin_question_add():
    if request.method == 'POST':
        new_q = Question(
            question_id=request.form.get('question_id'),
            title=request.form.get('title'),
            description=request.form.get('description'),
            input_format=request.form.get('input_format'),
            constraints=request.form.get('constraints'),
            output_format=request.form.get('output_format'),
            sample_input=request.form.get('sample_input'),
            sample_output=request.form.get('sample_output'),
            explanation=request.form.get('explanation'),
            difficulty=request.form.get('difficulty')
        )
        db.session.add(new_q)
        db.session.commit()
        flash('Question published successfully!')
        return redirect(url_for('main.admin_panel'))
    return redirect(url_for('main.admin_panel'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('main.admin_panel'))
        flash('Invalid Credentials')
    return render_template('admin_login.html')

@bp.route('/admin/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_question(id):
    questions = Question.query.get_or_404(id)
    if request.method == 'POST':
        # Update fields individually or use a form library (keeping it simple for now)
        questions.question_id = request.form.get('question_id')
        questions.title = request.form.get('title')
        questions.description = request.form.get('description')
        questions.input_format = request.form.get('input_format')
        questions.constraints = request.form.get('constraints')
        questions.output_format = request.form.get('output_format')
        questions.sample_input = request.form.get('sample_input')
        questions.sample_output = request.form.get('sample_output')
        questions.explanation = request.form.get('explanation')
        questions.difficulty = request.form.get('difficulty')
        
        db.session.commit()
        return redirect(url_for('main.admin_panel'))
    return render_template('edit_questions.html', questions=questions)

@bp.route('/admin/delete_question/<int:id>')
@login_required
def delete_question(id):
    db.session.delete(Question.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('main.admin_panel'))

@bp.route('/admin/delete_msg/<int:id>')
@login_required
def delete_msg(id):
    db.session.delete(Message.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('main.admin_panel'))

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Compiler Run Module - Refactored to use Piston API
@bp.route("/run", methods=["POST"])
def run_code():
    data = request.json
    code = data.get("code")
    lang = data.get("language")
    user_input = data.get("input", "")
    
    if not code or not lang:
        return jsonify({"output": "", "error": "Missing code or language"})

    # Use the Piston API runner
    result = execute_code(lang, code, user_input)
    
    return jsonify(result)
