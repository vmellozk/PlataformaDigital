from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'chave_secreta'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY,
                       email TEXT UNIQUE,
                       password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses
                      (id INTEGER PRIMARY KEY,
                       question1 TEXT,
                       question2 TEXT,
                       question3 TEXT,
                       question4 TEXT,
                       question5 TEXT,
                       question6 TEXT,
                       question7 TEXT,
                       question8 TEXT,
                       question9 TEXT,
                       question10 TEXT,
                       FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

@app.route('/')
def vendas():
    return render_template('templates/vendas.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))

        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return redirect(url_for('templates/register.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM user WHERE email = ? AND password = ?', (email, password))

            user = cursor.fetchone() # --> 
            conn.close()

            if user:
                session['user_id'] = user[0]
                return redirect(url_for('vendas'))
            return render_template('templates/login.html')        

@app.route('/submit', methods=['POST'])  
def submit():
    if 'user_id' in session:
        user_id = session['user_id']
        data = (
            user_id,
            request.form['question1'],
            request.form['question2'],
            request.form['question3'],
            request.form['question4'],
            request.form['question5'],
            request.form['question6'],
            request.form['question7'],
            request.form['question8'],
            request.form['question9'],
            request.form['question10']
        )

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO survey_responses (user_id, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

        conn.commit()
        conn.close()

        generate_ebook(user_id)

        return redirect(url_for('vendas'))
    return redirect(url_for('login'))
    
def generate_ebook(user_id):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(f"SELECT * FROM survey_responses WHERE user_id = {user_id}", conn)
    conn.close()

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Survey Responses eBook', 0, 1, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(10)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_chapter(self, title, body):
            self.add_page()
            self.chapter_title(title)
            self.chapter_body(body)

    pdf = PDF()
    for vendas, row in df.iterrows():
        title = f"Response {vendas + 1}"
        body = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
        pdf.add_chapter(title, body)

    pdf.output(f'survey_responses_ebook_{user_id}.pdf')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)