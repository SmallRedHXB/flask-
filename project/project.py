from flask import Flask, render_template, request, redirect, url_for, session
import config
from extx import db
from models import User, Question, Answer
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    content = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **content)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', res = '用户名或密码错误，请重新核对填写。')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        phone = phone.strip()
        if (len(phone) != 11) or (phone[0:1] != 1):
            return render_template('register.html', res = '手机号码错误，请重新输入手机号。')
        user = User.query.filter(User.phone == phone).first()
        if user:
            return render_template('register.html', res = '手机号码已被注册，请重新输入新的手机号。')
        else:
            if password != password1:
                return render_template('register.html', res = '两次密码不一致，请重新核对填写。')
            else:
                user = User(phone = phone, username = username, password = password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    userid = session.get('user_id')
    if not userid:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        if (title != '') and (content != ''):
            question = Question(title = title, content = content, author_id = userid)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('question'))

@app.route('/quesdetail/<question_id>')
def quesdetail(question_id):
    userid = session.get('user_id')
    if not userid:
        return redirect(url_for('login'))
    question = Question.query.filter(Question.id == question_id).first()
    if question:
        question_num = len(question.answers)
        return render_template('quesdetail.html', question = question, question_num = question_num)
    else:
        return 'error'


@app.route('/answer', methods = ['POST'])
def answer():
    if request.method == 'POST':
        userid = session.get('user_id')
        if not userid:
            return redirect(url_for('login'))
        content = request.form.get('anwser')
        question_id = request.form.get('question_id')
        # answer = Answer(content = content, question_id = question_id, author_id = userid)
        answer = Answer(content=content)
        question = Question.query.filter(Question.id == question_id).first()
        user = User.query.filter(User.id == userid).first()
        answer.question = question
        answer.author = user
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('quesdetail', question_id = question_id))

@app.route('/search')
def search():
    search_con = request.args.get('q')
    questions = Question.query.filter(or_(Question.content.contains(search_con),
                              Question.title.contains(search_con))).order_by('-create_time')
    return render_template('index.html', questions=questions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def context_processor_():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
        else:
            return {}
    else:
        return {}

if __name__ == '__main__':
    app.run()