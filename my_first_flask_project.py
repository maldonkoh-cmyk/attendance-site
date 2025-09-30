from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)

@app.route('/teacher-about')
def teacher_about():
    return render_template('teacher_about.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    status = request.form['status']
    class_name = request.form.get('class', 'Alevel 2')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (name, status, class) VALUES (?, ?, ?)", (name, status, class_name))
    conn.commit()
    conn.close()
    return redirect('/')


    
@app.route('/')
def index():
    return render_template('index.html', title="Attendance Dashboard")

@app.route('/about')
def about():
    return render_template('about.html')

def init_db():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance(
              id INTEGER PRIMARY KEY, 
              name TEXT NOT NULL,
              status TEXT NOT NULL,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              "class" TEXT NOT NULL DEFAULT 'Alevel 2'
    )''')
    conn.commit()
    conn.close()

init_db()   

def submit():
    name=request.form['name']
    status=request.form['status']
    class_name=request.form['class']
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("INSERT INTO attendance (name, status, class) VALUES (?, ?, ?)", (name, status, class_name))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/teacher')
def teacher():
    key=request.args.get('key')
    if key != 'abc123':
        return "Access denied", 403
    
    filter_date=request.args.get('date')
    conn=sqlite3.connect('database.db')
    c=conn.cursor()

    if filter_date:
        c.execute("SELECT * FROM attendance WHERE DATE(timestamp)=? ORDER BY timestamp DESC", (filter_date,))
    else:
        c.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    
    records=c.fetchall()
    conn.close()
    return render_template('teacher.html', records=records,filter_date=filter_date)

if __name__ == '__main__':
    app.run(debug=True)
