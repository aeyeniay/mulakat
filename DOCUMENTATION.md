# 📚 INTERVIEW QUESTION PREPARATION SYSTEM - DOCUMENTATION GUIDE

## 🎯 OVERVIEW

This documentation explains the purpose, scope, and technical details of each file in the system.

## 📁 FILE STRUCTURE AND DOCUMENTATION

### 🖥️ BACKEND (Python/FastAPI)

#### 📄 `backend/app/main.py`
- **Purpose**: Main API endpoints and business logic
- **Scope**: 37 API endpoints, CORS configuration, routing
- **Input**: HTTP requests, JSON data
- **Output**: JSON responses, Word/ZIP files
- **Lines of Code**: 1,370

#### 🔧 `backend/app/utils.py`
- **Purpose**: AI integration and helper functions
- **Scope**: OpenAI API, question generation, JSON parsing, difficulty system
- **Input**: Job posting data, role configurations
- **Output**: Generated questions and answer keys
- **Lines of Code**: 550

#### 🗄️ `backend/app/models.py`
- **Purpose**: Database models and relationships
- **Scope**: 9 SQLAlchemy models, properties, relationships
- **Input**: ORM queries
- **Output**: Database objects
- **Lines of Code**: 294

#### 🔗 `backend/app/database.py`
- **Purpose**: Database connection management
- **Scope**: SQLAlchemy engine, session factory, dependency injection
- **Input**: Environment variables
- **Output**: Database sessions
- **Lines of Code**: 64

#### 📦 `backend/requirements.txt`
- **Purpose**: Python package dependencies
- **Scope**: 8 main packages with versions
- **Categories**: Web framework, AI, Database, File processing

### 🌐 FRONTEND (React.js)

#### ⚛️ `frontend/src/components/Step2.jsx`
- **Purpose**: Role/position management interface
- **Scope**: CRUD operations, form validation, state management
- **Input**: Contract ID, user interactions
- **Output**: Saved role data
- **Lines of Code**: 409

## 🔧 TECHNICAL ARCHITECTURE

### Backend Stack:
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite + SQLAlchemy ORM
- **AI**: OpenAI GPT-4o-mini
- **File Processing**: python-docx
- **Server**: Uvicorn ASGI

### Frontend Stack:
- **Framework**: React.js
- **State Management**: useState/useEffect hooks
- **HTTP Client**: Axios
- **UI**: Custom CSS + Bootstrap-like styling

## 📊 DATA FLOW DIAGRAM

```
👤 USER INPUT → 🌐 FRONTEND → 📡 API CALLS → 🖥️ BACKEND → 🗄️ DATABASE
                                                ↓
🤖 OPENAI API ← 🔧 UTILS.PY ← 📊 BUSINESS LOGIC ← 📄 MAIN.PY
                                                ↓
📄 WORD FILES ← 📁 FILE GENERATION ← 💾 GENERATED QUESTIONS
```

## 🚀 INSTALLATION AND RUNNING

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m app.main
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 📝 DOCUMENTATION STANDARDS

Each file includes the following sections:
- 📋 **FILE PURPOSE**: What does it do?
- 🎯 **SCOPE**: Which features?
- 📊 **DATA FLOW**: Input/output details
- 🔧 **TECHNICAL INFO**: Technologies used
- ⚙️ **FUNCTIONS**: Main function list
- 👨‍💻 **DEVELOPER**: Project information

## 🔒 SECURITY NOTES

- OpenAI API key must be stored in environment variables
- CORS settings should be reviewed in production
- Database connections must be secured with SSL
- File upload size limits should be enforced

## 📞 SUPPORT

For technical questions, please review the documentation. Detailed explanations are provided at the beginning of each file.

---

👨‍💻 **Developer**: AI-Assisted Development

📅 **Date**: 08.2025

🔄 **Version**: 1.0.0
