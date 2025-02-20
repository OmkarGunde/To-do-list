from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = 'mysecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)  

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)  

# Initialize database (only for first-time setup)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')

        if title.strip():  # Prevent empty titles
            new_task = Todo(title=title.strip())  
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully', 'success')
        else:
            flash('Title cannot be empty', 'danger')

        return redirect(url_for('index'))  

    tasks = Todo.query.order_by(Todo.id.desc()).all()  
    return render_template('index.html', groceries=tasks)

@app.route('/update/<int:todo_id>', methods=['POST'])
def update(todo_id):
    task = Todo.query.get_or_404(todo_id)

    title = request.form.get('title')
    if title.strip():
        task.title = title.strip()
        db.session.commit()
        flash('Task updated successfully', 'success')
    else:
        flash('Title cannot be empty', 'danger')

    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    task = Todo.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_task(todo_id):
    task = Todo.query.get_or_404(todo_id)
    task.completed = not task.completed  
    db.session.commit()
    flash('Task status updated successfully', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
