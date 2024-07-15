from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses
                   (id INTEGER PRIMARY KEY,
                   question 1 TEXT,
                   question 2 TEXT,
                   question 3 TEXT,
                   question 4 TEXT,
                   question 5 TEXT,
                   question 6 TEXT,
                   question 7 TEXT,
                   question 8 TEXT,
                   question 9 TEXT,
                   question 10 TEXT,
                   )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('vendas.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = (
            request.form['question1'],
            request.form['question2'],
            request.form['question3'],
            request.form['question4'],
            request.form['question5'],
            request.form['question6'],
            request.form['question7'],
            request.form['question8'],
            request.form['question9'],
            request.form['question10'],
        )

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO survey_responses (question1, question2, question3, question4, question5, question6, question7, question8, question9, question10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
