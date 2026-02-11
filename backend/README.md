# 🗞️ AI News Portal

An intelligent news portal built with FastAPI, MongoDB, and AI chatbot capabilities.

## 🌟 Features

- **FastAPI Backend** - High-performance REST API
- **MongoDB Database** - Persistent storage for news articles
- **Web Scraper** - Automatic news collection from TechCrunch, The Verge, BBC, CNN
- **AI Chatbot** - Interactive chatbot to answer questions about news
- **Real-time Updates** - Latest news from multiple sources

## 🛠️ Technologies Used

- **Backend**: FastAPI, Python 3.14
- **Database**: MongoDB Atlas
- **Web Scraping**: BeautifulSoup4, Feedparser
- **AI**: Mock Chatbot (OpenAI API compatible)

## 📦 Installation

### Prerequisites
- Python 3.10+
- MongoDB Atlas account

### Setup

1. Clone the repository:
```bash
git clone https://github.com/avoithic-aiesh/news-portal.git
cd news-portal
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```
MONGODB_URL=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_key_optional
```

5. Run the server:
```bash
cd backend
python3 -m uvicorn main:app --reload
```

6. Open browser: http://localhost:8000/docs

## 🚀 API Endpoints

- `GET /` - API information
- `GET /news` - Get all news articles  
- `POST /news` - Add news article
- `POST /scrape` - Scrape news from sources
- `POST /chat` - Chat with AI about news
- `DELETE /news` - Delete all articles
- `DELETE /news/{id}` - Delete specific article

## 📁 Project Structure
```
News_Portal/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   ├── database.py       # MongoDB connection
│   ├── scraper.py        # Web scraping logic
│   ├── chatbot.py        # AI chatbot
│   └── test_db.py        # Database tests
├── .env                  # Environment variables (not tracked)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

Test the scraper:
```bash
cd backend
python3 scraper.py
```

Test the chatbot:
```bash
python3 chatbot.py
```

Test database connection:
```bash
python3 test_db.py
```

## 🎓 Academic Project

This project was built as part of an internship-level academic assignment demonstrating:
- RESTful API design
- Database integration
- Web scraping techniques
- AI/ML integration
- Full-stack development skills

## 👨‍💻 Author

**Aieshma Khadka**
- GitHub: [@avoithic-aiesh](https://github.com/avoithic-aiesh)

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- FastAPI Documentation
- MongoDB Documentation
- BeautifulSoup4 Documentation
- OpenAI API Documentation