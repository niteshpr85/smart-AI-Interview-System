from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db
from ai_engine import evaluate_answer, generate_questions
import base64
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "secret123"   # required for login session
@app.route('/set_lang', methods=['POST'])
def set_lang():
    lang = request.form.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or '/')

# Initialize database
init_db()


# ---------------- DB CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect('interview.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            conn.close()
            return "⚠️ User already exists!"

        conn.close()
        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "❌ Invalid username or password"

    return render_template('login.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------------- CREATE ----------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        question = request.form['question'].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Prevent duplicate
        cursor.execute("SELECT * FROM questions WHERE question = ?", (question,))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute("INSERT INTO questions (question) VALUES (?)", (question,))
            conn.commit()

        conn.close()
        return redirect('/interview')

    return render_template('add_question.html')


# ---------------- READ + AI ----------------
@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    feedback = None
    score = None

    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')

        if question and answer:
            # 🔥 AI evaluation
            lang = session.get('lang', 'en')
            feedback = evaluate_answer(question, answer, lang)

            # 🎯 Extract score from feedback
            score = 5  # default

            if "10" in feedback:
                score = 10
            elif "9" in feedback:
                score = 9
            elif "8" in feedback:
                score = 8
            elif "7" in feedback:
                score = 7
            elif "6" in feedback:
                score = 6

            # 💾 Save answer
            cursor.execute(
                "INSERT INTO answers (question, answer, feedback) VALUES (?, ?, ?)",
                (question, answer, feedback)
            )

            # 💾 Save score separately (for dashboard analytics)
            cursor.execute(
                "INSERT INTO scores (score) VALUES (?)",
                (score,)
            )

            conn.commit()

    # 📋 Fetch questions
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    conn.close()

    return render_template(
        'interview.html',
        questions=questions,
        feedback=feedback,
        score=score
    )

# ---------------- UPDATE ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        new_question = request.form['question'].strip()

        # Prevent duplicate update
        cursor.execute("SELECT * FROM questions WHERE question = ?", (new_question,))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute(
                "UPDATE questions SET question=? WHERE id=?",
                (new_question, id)
            )
            conn.commit()

        conn.close()
        return redirect('/interview')

    cursor.execute("SELECT * FROM questions WHERE id=?", (id,))
    question = cursor.fetchone()
    conn.close()

    return render_template('edit_question.html', question=question)


# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_question(id):
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM questions WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/interview')
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 📊 Total Questions
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]

    # 📊 Total Answers
    cursor.execute("SELECT COUNT(*) FROM answers")
    total_answers = cursor.fetchone()[0]

    # ⭐ AVG SCORE (THIS IS WHERE YOU ADD IT)
    cursor.execute("SELECT AVG(score) FROM scores")
    avg_score = cursor.fetchone()[0] or 0

    conn.close()

    return render_template(
        'dashboard.html',
        total_questions=total_questions,
        total_answers=total_answers,
        avg_score=int(avg_score)   # convert to int for clean UI
    )
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        role = request.form['role']
        file = request.files.get('resume')
        text = ""
        if file and file.filename != '':
            pdf = pypdf2.PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        role_text = role + " " + text.strip()
        lang = session.get('lang', 'en')
        questions = generate_questions(role_text, lang)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM questions")

        for q in questions:
            cursor.execute("INSERT INTO questions (question) VALUES (?)", (q,))

        conn.commit()
        conn.close()

        return redirect('/interview')

    return render_template('generate.html')
@app.route('/download')
def download_pdf():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM answers")
    data = cursor.fetchall()
    conn.close()

    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Interview Report", styles['Title']))

    for row in data:
        content.append(Paragraph(f"Question: {row[1]}", styles['Normal']))
        content.append(Paragraph(f"Answer: {row[2]}", styles['Normal']))
        content.append(Paragraph(f"Feedback: {row[3]}", styles['Normal']))
        content.append(Paragraph("----------------------", styles['Normal']))

    doc.build(content)

    return redirect('/dashboard')
@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.json['image']

    image_data = data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    with open("static/captured.jpg", "wb") as f:
        f.write(image_bytes)

    return "Saved"

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)