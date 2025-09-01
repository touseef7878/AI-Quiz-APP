from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import QuizResult, Quiz, db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics and recent activity"""
    
    # Get user statistics
    results = QuizResult.query.filter_by(user_id=current_user.id).all()
    
    # Calculate statistics
    stats = {
        'total_quizzes': len(results),
        'average_score': 0,
        'best_score': 0,
        'total_score': 0,
        'difficulty_stats': {'simple': 0, 'medium': 0, 'hard': 0},
        'recent_results': []
    }
    
    if results:
        scores = [r.score for r in results]
        stats['average_score'] = round(sum(scores) / len(scores), 1)
        stats['best_score'] = max(scores)
        stats['total_score'] = sum(scores)
        
        # Get difficulty breakdown
        difficulty_query = db.session.query(
            Quiz.difficulty, 
            func.avg(QuizResult.score).label('avg_score'),
            func.count(QuizResult.id).label('count')
        ).join(QuizResult).filter(
            QuizResult.user_id == current_user.id
        ).group_by(Quiz.difficulty).all()
        
        for difficulty, avg_score, count in difficulty_query:
            stats['difficulty_stats'][difficulty] = {
                'count': count,
                'average_score': round(float(avg_score), 1)
            }
        
        # Get recent results (last 5)
        recent_results = QuizResult.query.filter_by(user_id=current_user.id)\
                                        .order_by(QuizResult.taken_at.desc())\
                                        .limit(5).all()
        stats['recent_results'] = [r.to_dict() for r in recent_results]
    
    return render_template('main/dashboard.html', stats=stats)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')
