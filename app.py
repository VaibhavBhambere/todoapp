from datetime import datetime
from flask import Flask, redirect,render_template, request
app= Flask(__name__)



from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):
    sr_no=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    description=db.Column(db.String)
    

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        sr=request.form['sr']
        tit=request.form['title']
        des=request.form['des']
        data=Todo(sr_no=sr, title=tit,description=des)
        db.session.add(data)
        db.session.commit()

        
    return render_template('home.html')

@app.route('/display',methods=['GET', 'POST'])
def display():
    alltodo=Todo.query.all()

    return render_template('display.html',alltodo=alltodo)

@app.route('/delete/<sr>', methods=['GET', 'POST','DELETE'])
def delete(sr):
    todo=Todo.query.get(pk=sr)
    db.session.delete(todo)   
    db.session.commit()
    return redirect('/display')

@app.route('/update/<sr>', methods=['GET', 'POST','DELETE'])
def update(sr):
    if request.method == 'POST':  
        
        tit=request.form['title']
        des=request.form['des']
        todo=Todo.query.get(sr)
        todo.title=tit
        todo.description=des
        db.session.add(todo)
        db.session.commit()
        return redirect('/display')

    todo=Todo.query.get(sr)
    return render_template('update.html',todo=todo)

app.run(debug=True)


