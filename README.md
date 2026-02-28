# 🧠 AI Quiz Application

A modern, intelligent quiz platform powered by Google's Gemini AI that generates dynamic quizzes on any topic with three difficulty levels.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **AI-Powered Quiz Generation**: Leverages Google Gemini AI to create unique, contextual quizzes
- **Multiple Difficulty Levels**: Choose from Simple, Medium, or Hard difficulty
- **User Authentication**: Secure registration and login system
- **Progress Tracking**: Comprehensive dashboard with statistics and performance analytics
- **Quiz History**: Review past quiz attempts and track improvement
- **Detailed Results**: Get explanations for correct answers after quiz completion
- **Responsive Design**: Modern, dark-themed UI that works on all devices
- **Real-time Scoring**: Instant feedback on quiz performance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-quiz-app
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Edit the `.env` file and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

To get a Gemini API key:
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Create a new API key

6. **Initialize the database**
```bash
python app.py
```

The application will automatically create the database on first run.

7. **Access the application**

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
ai-quiz-app/
│
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── ai_service.py          # AI quiz generation logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
│
├── routes/
│   ├── main.py           # Main routes (home, dashboard)
│   ├── auth.py           # Authentication routes
│   └── quiz.py           # Quiz-related routes
│
├── templates/
│   ├── base.html         # Base template
│   ├── main/             # Main page templates
│   ├── auth/             # Authentication templates
│   ├── quiz/             # Quiz templates
│   └── errors/           # Error page templates
│
├── static/
│   ├── css/
│   │   └── modern.css    # Custom styles
│   └── js/
│       └── main.js       # JavaScript functionality
│
└── instance/
    └── site.db           # SQLite database
```

## 🎯 Usage

### Creating a Quiz

1. Register or log in to your account
2. Navigate to "Create Quiz" from the dashboard
3. Enter a topic (e.g., "Python Programming", "World History")
4. Select difficulty level (Simple, Medium, or Hard)
5. Click "Generate Quiz" and wait for AI to create questions
6. Start taking the quiz!

### Taking a Quiz

- Read each question carefully
- Select one answer from the four options
- Navigate between questions using Previous/Next buttons
- Submit when all questions are answered
- View detailed results with explanations

### Viewing Statistics

- Access your dashboard to see:
  - Total quizzes taken
  - Average score
  - Best score
  - Performance by difficulty level
  - Recent quiz history

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Flask-Migrate**: Database migrations
- **Google Generative AI**: Quiz generation

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icons

### Database
- **SQLite**: Lightweight database for development
- Easily upgradeable to PostgreSQL/MySQL for production

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-change-in-production` |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `QUIZ_QUESTIONS_COUNT` | Number of questions per quiz | `10` |
| `FLASK_ENV` | Environment mode | `development` |

### Database Configuration

The application uses SQLite by default. To use a different database, modify `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Registration timestamp

### Quizzes Table
- `id`: Primary key
- `topic`: Quiz topic
- `difficulty`: Difficulty level (simple/medium/hard)
- `created_at`: Creation timestamp

### Questions Table
- `id`: Primary key
- `quiz_id`: Foreign key to quizzes
- `question_text`: Question content
- `option_a`, `option_b`, `option_c`, `option_d`: Answer options
- `correct_option`: Correct answer (A/B/C/D)
- `explanation`: Answer explanation
- `question_number`: Question order

### Quiz Results Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `quiz_id`: Foreign key to quizzes
- `score`: Quiz score
- `user_answers`: JSON of user's answers
- `taken_at`: Completion timestamp

## 🎨 Features in Detail

### AI Quiz Generation
The application uses Google's Gemini 2.0 Flash model to generate contextual, relevant questions based on:
- User-specified topic
- Selected difficulty level
- Diverse question types covering different aspects

### User Dashboard
Comprehensive analytics including:
- Total quizzes taken
- Average performance score
- Best score achieved
- Breakdown by difficulty level
- Recent quiz history with quick access

### Results Analysis
After completing a quiz, users receive:
- Overall score and percentage
- Question-by-question breakdown
- Correct answers highlighted
- Detailed explanations for learning
- Option to retake or try new topics

## 🔒 Security Features

- Password hashing using Werkzeug security
- Session management with Flask-Login
- CSRF protection
- SQL injection prevention through SQLAlchemy ORM
- Environment variable protection for sensitive data

## 🚀 Deployment

### Production Checklist

1. **Update environment variables**
   - Set a strong `SECRET_KEY`
   - Use production database
   - Set `FLASK_ENV=production`

2. **Database migration**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

3. **Use a production server**
   - Gunicorn (recommended)
   - uWSGI
   - Waitress

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

4. **Set up reverse proxy** (Nginx/Apache)

5. **Enable HTTPS** with SSL certificate

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- [ ] Multiple quiz formats (True/False, Fill in the blanks)
- [ ] Timed quiz mode
- [ ] Leaderboard system
- [ ] Quiz sharing functionality
- [ ] Export results as PDF
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Custom quiz creation without AI

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [touseefurrehman554@gmail.com]

## 🙏 Acknowledgments

- Google Gemini AI for quiz generation
- Flask community for excellent documentation
- Bootstrap team for the responsive framework
- All contributors and users

---

**Made with ❤️ by Touseef**
