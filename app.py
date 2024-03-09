from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.task} - {self.description}"

with app.app_context() :
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def ToDo() :
    # todo = Todo(task="Learn Flask", description="Complete Flask tutorial and implementation of Code With Harry")
    # db.session.add(todo)
    # db.session.commit()

    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        newtask = Todo(task=task, description=desc)
        db.session.add(newtask)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        newtask = Todo.query.filter_by(sno=sno).first()
        newtask.task = task
        newtask.description = desc
        db.session.add(newtask)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)