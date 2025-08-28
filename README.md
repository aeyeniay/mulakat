# Interview Question Preparation System

## About the Project

This system is designed as an interview question preparation application to be used in public institutions during the recruitment processes of contracted IT personnel. By leveraging artificial intelligence technology, it generates customized interview questions based on position, level, and area of expertise, and exports them in Word file format.

## Features

- Five-step question generation process
- Role-based question configuration
- Automatic question generation (OpenAI GPT-4o-mini)
- Expected answer keys
- Editable questions
- Candidate and jury booklets in Word format
- Difficulty level management (2x, 3x, 4x multipliers)

## Technologies Used

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite + SQLAlchemy ORM 2.0.23
- **AI Integration**: OpenAI GPT-4o-mini API
- **Document Processing**: python-docx 1.1.0
- **Server**: Uvicorn 0.24.0

### Frontend
- **Framework**: React.js + Vite
- **HTTP Client**: Axios
- **Styling**: CSS3 + Bootstrap benzeri responsive tasarım

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- NPM package manager
- OpenAI API key

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Configuration

Update your OpenAI API key in the `backend/app/utils.py` file:

```python
client = OpenAI(
    api_key="your-api-key-here",
    timeout=60.0,
    max_retries=3
)
```

## Usage

### 1. Job Information
Enter the job title and general requirements. The system automatically generates a unique ID.

### 2. Role Definitions
- Position name and description
- Salary multiplier (2x, 3x, 4x)
- Number of positions
- Special requirements

### 3. Question Configuration
Define question types and quantities for each role:
- Professional Experience Questions
- Theoretical Knowledge Questions
- Practical Application Questions

### 4. Question Generation
Click the "Generate Questions" button to start the AI-powered question generation process. You can edit the generated questions individually.

### 5. Dosya İndirme
Download separate Word-format booklets for candidates (S1, S2…) and jury members (C1, C2…) for each role.

## Project Structure

```
mulakat_soru/
├── backend/
│   ├── app/
│   │   ├── main.py          # Ana API endpoint'leri
│   │   ├── models.py        # Veritabanı modelleri
│   │   ├── utils.py         # AI entegrasyonu ve yardımcı fonksiyonlar
│   │   └── database.py      # Veritabanı bağlantı yönetimi
│   └── requirements.txt     # Python bağımlılıkları
├── frontend/
│   ├── src/
│   │   ├── components/      # React bileşenleri
│   │   ├── App.jsx         # Ana uygulama
│   │   └── App.css         # Stil dosyaları
│   └── package.json        # Node.js bağımlılıkları
└── README.md
```

## API Endpoints

- `/api/step1/` - Job management
- `/api/step2/` - Role management
- `/api/step3/` - Question configuration
- `/api/step4/` - Question generation
- `/api/step5/` - Word file generation
- `/api/system/` - System information

## Database

The system uses an SQLite database and includes the following tables:
- contracts
- roles
- question_types
- role_question_configs
- questions

## Development

For detailed technical documentation, please refer to the comments at the beginning of each file. The DOCUMENTATION.md file provides a comprehensive overview of the system architecture.

## Contact

Ahmet Erdem Yeniay  
aeyeniay@gmail.com

## Lisans

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Development Date**: 08.2025  
**Version**: 1.0.0 
