# 🤖 AI Learning Content Agent

An AI-powered personalized learning platform that generates customized lessons and interactive quizzes based on the learner's topic, skill level, and learning goal.

The application uses an agentic AI workflow with LangGraph and LangChain, powered by Llama 3.1 8B through Ollama. Generated learning content is stored in SQLite and can be accessed later through the learning history.

---

## 🚀 Features

- 📚 Personalized AI-generated lessons
- 🎯 Learning goal-based content generation
- 🎓 Beginner, Intermediate, and Advanced levels
- 📝 AI-generated multiple-choice quizzes
- ✅ Interactive quiz system
- 📊 Automatic quiz score calculation
- 📈 Performance analysis
- 💡 Learning recommendations
- 🕒 Learning history
- 🔄 Access previously generated lessons and quizzes
- 🌐 FastAPI REST APIs
- 🤖 LangGraph agent workflow
- 🦙 Local LLM using Ollama and Llama 3.1 8B
- 💾 SQLite database
- 📖 Swagger API documentation

---

## 🧠 How It Works

The user provides:

- Topic
- Learner Level
- Learning Goal

The AI agent then generates personalized learning content.

```text
User Input
    ↓
FastAPI
    ↓
LangGraph Agent
    ↓
Generate Personalized Lesson
    ↓
Generate Quiz
    ↓
Store in SQLite
    ↓
Display Lesson + Quiz
    ↓
Quiz Score
    ↓
Performance Analysis
    ↓
Learning Recommendation

---

🛠️ Technologies Used

- Python
- FastAPI
- LangGraph
- LangChain
- Ollama
- Llama 3.1 8B
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript

---

▶️ How to Run

1. Install dependencies
pip install -r requirements.txt

2. Start Ollama
ollama run llama3.1:8b

3. Start the FastAPI server
uvicorn app.main:app --reload

4. Open the application
http://127.0.0.1:8000

API Documentation
http://127.0.0.1:8000/docs

👨‍💻 Author
Nagendra
BE CSE – Artificial Intelligence & Machine Learning
