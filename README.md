# ✨ Astro AI - Your Personal Astrological Assistant

A modern astrology application that generates birth charts, provides daily horoscopes, and answers your astrology questions using AI. Built with FastAPI backend and React frontend.

## 🌟 Features

- **Birth Chart Generation**: Enter your birth details and get a complete natal chart analysis
- **AI-Powered Interpretations**: Get personalized astrological insights using Google's Gemini AI
- **Daily Horoscopes**: Receive daily astrological guidance
- **Q&A Interface**: Ask any astrology question and get intelligent responses
- **Modern UI**: Clean, responsive design built with React and Tailwind CSS
- **Context-Aware**: AI remembers your birth chart when answering questions

## 🔧 Requirements

- Python 3.8+
- Node.js 16+ and npm
- Google Gemini API key (for AI features)

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
cd backend
python api.py
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The React app will be available at `http://localhost:3000`

## 📋 Setup Instructions

### Backend Configuration

1. **API Keys**: The application uses Google Gemini API. Make sure you have a valid API key configured in `tools/gemini_client.py`:
   ```python
   genai.configure(api_key="your-api-key-here")
   ```

2. **Database**: The app uses SQLite databases that are automatically created in the `data/` and `cache/` directories.

### Frontend Configuration

The frontend is pre-configured to communicate with the backend at `http://localhost:8000`. If you change the backend port, update the API URLs in the React components.

## 🏗️ Architecture

### Backend (Python)
- **FastAPI**: Modern web API framework
- **LangGraph**: Workflow orchestration for astrology calculations
- **Google Gemini**: AI-powered interpretations and Q&A
- **Kerykeion**: Astrology calculations library
- **SQLAlchemy**: Database operations

### Frontend (React)
- **React 18**: Modern UI framework
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Works on desktop and mobile

### Data Flow
1. User inputs birth details through React form
2. Frontend sends POST request to FastAPI backend
3. Backend processes data through LangGraph workflow:
   - Validates input data
   - Geocodes birth location
   - Calculates timezone and UTC time
   - Generates natal chart using Kerykeion
   - Fetches daily horoscope
   - Creates AI interpretation using Gemini
   - Saves to database
4. Results returned to frontend and displayed

## 🛠️ Development

### Running in Development Mode

**Backend:**
```bash
# From project root
python -m uvicorn backend.api:api --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
# From frontend directory
npm run dev
```

### Project Structure

```
astro_ai/
├── backend/
│   ├── api.py              # FastAPI application
│   ├── graph.py            # LangGraph workflow
│   ├── state.py            # Pydantic models
│   ├── nodes/              # Workflow nodes
│   └── utils/              # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── tools/                  # External API clients
├── data/                   # SQLite database
├── cache/                  # Geocoding cache
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 📱 Usage

1. **Generate Birth Chart**:
   - Go to the "Birth Chart" tab
   - Enter your name, birth date, time, and place
   - Click "Generate Birth Chart"
   - View your natal chart, horoscope, and AI interpretation

2. **Ask Questions**:
   - Go to the "Ask Questions" tab
   - Type any astrology-related question
   - Get AI-powered responses
   - If you have generated a birth chart, questions will be context-aware

## 🌐 API Endpoints

- `GET /` - Health check
- `POST /birth-chart` - Generate birth chart and interpretation
- `POST /ask-question` - Ask astrology questions

## 🔒 Security

- API keys are stored in source code (update for production use)
- CORS is enabled for localhost development
- Input validation using Pydantic models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational and personal use.

---

**Built with ❤️ using modern web technologies and AI**
