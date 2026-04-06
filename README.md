# 🤖 Smart AI Interview System

AI-powered full-stack interview preparation platform with multi-language support.

## 🚀 Key Features


https://github.com/user-attachments/assets/c2bf6b04-0536-44a5-b059-1957946c84c9


- **🔐 Complete User Authentication** (Register/Login/Logout with sessions)
- **🧠 AI Question Generation** (Ollama LLaMA3, role-based, PDF resume upload/parsing)
- **🎤 Voice Interview** (Speech-to-Text input, real-time transcription)
- **🎥 Video Interview** (Live camera, image capture)
- **⏱ Timer** (6-minute countdown per question)
- **🤖 AI Evaluation** (Score 1-10 + feedback)
- **📊 Analytics Dashboard** (Questions answered, avg score)
- **📄 PDF Report** (Download interview summary)
- **🌐 Multi-Language** (English/Hindi toggle - UI, prompts, feedback)
- **📱 Responsive UI** (TailwindCSS)
- 

## 🛠 Tech Stack
<img width="1906" height="859" alt="Screenshot 2026-04-06 192642" src="https://github.com/user-attachments/assets/956137ef-1a8e-4bb5-aed1-17aafd07dff3" />


```<img width="1895" height="870" alt="Screenshot 2026-04-06 192759" src="https://github.com/user-attachments/assets/f7fd2617-e2b0-4522-b66e-0ef0be27a93d" />


<img width="1889" height="493" alt="Screenshot 2026-04-06 192821" src="https://github.com/user-attachments/assets/c555320e-586d-4704-97f2-cfaaa7c13e02" />

Backend: Flask (Python)
DB: SQLite
AI: Ollama (llama3 model)
PDF: pypdf2, reportlab
Frontend: Jinja2, TailwindCSS
Media: WebRTC APIs (camera/mic)
```

## 📦 Setup & Run

<img width="1889" height="493" alt="Screenshot 2026-04-06 192821" src="https://github.com/user-attachments/assets/dca6523d-e546-4ef8-bc3a-4c38b64afd32" />


<img width="1902" height="867" alt="Screenshot 2026-04-06 193045" src="https://github.com/user-attachments/assets/41d102d4-17d7-44f1-bc51-46451a541d74" />

1. **Virtual Env**
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. **Dependencies**
   ```
   pip install flask pypdf2 reportlab
   ```

3. **Ollama** (AI Model)
   ```
   ollama pull llama3
   ollama serve
   ```

4. **Run**
   ```
   python app.py
   ```
   Open http://127.0.0.1:5000

## 🎮 How to Use

1. **Register/Login**
2. **Generate** questions (enter role + optional resume PDF)
3. **Interview** (video/speech/timer/AI feedback)
4. **Dashboard** analytics
5. **Download** PDF report
6. **Toggle** EN/हिं for Hindi support

## 🗄 Database Schema
```
users(id, username, password)
questions(id, question)
answers(id, question, answer, feedback)
scores(id, score)
```

## 🎉 What's Fixed/Added
- Jinja2 template errors
- PyPDF2 dependency
- Multi-language (EN/Hindi)
- Session management
- Full CRUD operations

**Ready for production!** Deploy with Gunicorn + Nginx.
