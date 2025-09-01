# AI Quiz App

A comprehensive web application that generates AI-powered quizzes on any topic with three difficulty levels. Built with Flask, featuring user authentication, detailed analytics, and responsive design.

## 🧠 Features

- **AI-Powered Quiz Generation**: Create quizzes on any topic using advanced AI models
- **Three Difficulty Levels**: Simple, Medium, and Hard to match user expertise
- **User Authentication**: Secure registration, login, and user session management
- **Comprehensive Dashboard**: Track progress with detailed statistics and analytics
- **Detailed Results**: Instant feedback with explanations for each question
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **SQLite Database**: Robust data storage

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-quiz-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   ```
   
   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Database Setup**
   The SQLite database will be automatically created in the `instance/` folder when the application is run for the first time.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Application: http://localhost:5000

## 🏗️ Project Structure

```
ai-quiz-app/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── ai_service.py         # AI integration service
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
│
├── instance/            # Instance folder for SQLite database
│   └── site.db          # SQLite database file
│
├── routes/              # Application routes
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── main.py         # Main application routes
│   └── quiz.py         # Quiz-related routes
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── main/           # Main page templates
│   ├── auth/           # Authentication templates
│   ├── quiz/           # Quiz-related templates
│   └── errors/         # Error page templates
│
├── static/             # Static files
│   ├── css/           # Custom stylesheets
│   ├── js/            # JavaScript files
│   └── images/        # Image assets
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Required |
| `GEMINI_API_KEY` | Google Gemini API key for AI features | Required |
| `QUIZ_QUESTIONS_COUNT` | Number of questions per quiz | 10 |
| `RATE_LIMIT_PER_HOUR` | API rate limit per user | 50 |

### Database Setup

The application uses SQLite. The database schema is defined by SQLAlchemy models in `models.py` and is automatically created when the application runs for the first time.

## 🎯 How to Use

### For Users

1. **Register/Login**: Create an account or sign in
2. **Create Quiz**: Enter any topic and select difficulty level
3. **Take Quiz**: Answer 10 multiple-choice questions
4. **View Results**: Get detailed feedback with explanations
5. **Track Progress**: Monitor your performance in the dashboard

### For Developers

1. **Adding New AI Providers**: Modify `ai_service.py` to integrate other AI services
2. **Customizing Questions**: Adjust the prompt templates in `AIQuizGenerator`
3. **Styling**: Edit `static/css/style.css` for custom styling
4. **Database Changes**: Update `models.py` and create migration scripts

## 🎨 Technologies Used

### Backend
- **Flask 3.1.1** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **Flask-Migrate** - Database migrations
- **Google Gemini API** - AI quiz generation
- **Werkzeug** - Password hashing

### Frontend
- **HTML5 & CSS3** - Markup and styling
- **Bootstrap 5** - Responsive framework
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icons
- **Custom CSS** - Enhanced styling and animations

### Database
- **SQLite** - Primary database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature-name'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📞 Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**Happy Learning with AI Quiz App! 🧠✨**
