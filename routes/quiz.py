from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Quiz, Question, QuizResult, db
from ai_service import AIQuizGenerator, calculate_quiz_score
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            topic = data.get('topic')
            difficulty = data.get('difficulty')
        else:
            topic = request.form.get('topic')
            difficulty = request.form.get('difficulty')
        
        # Validation
        if not topic or not topic.strip():
            error_msg = 'Topic is required'
            if request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('quiz/create.html')
        
        if difficulty not in ['simple', 'medium', 'hard']:
            error_msg = 'Invalid difficulty level'
            if request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('quiz/create.html')
        
        try:
            # Generate quiz using AI
            ai_generator = AIQuizGenerator()
            quiz = ai_generator.generate_quiz(topic.strip(), difficulty)
            
            if quiz:
                if request.is_json:
                    return jsonify({
                        'success': True, 
                        'quiz_id': quiz.id,
                        'message': 'Quiz generated successfully!'
                    })
                flash('Quiz generated successfully!', 'success')
                return redirect(url_for('quiz.take_quiz', quiz_id=quiz.id))
            else:
                error_msg = 'Failed to generate quiz. Please try again.'
                if request.is_json:
                    return jsonify({'success': False, 'message': error_msg}), 500
                flash(error_msg, 'error')
                
        except Exception as e:
            error_msg = f'Error generating quiz: {str(e)}'
            if request.is_json:
                return jsonify({'success': False, 'message': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('quiz/create.html')

@quiz_bp.route('/take/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_number).all()
    
    # Convert questions to format without answers
    questions_data = [q.to_dict(include_answer=False) for q in questions]
    
    return render_template('quiz/take.html', quiz=quiz, questions=questions_data)

@quiz_bp.route('/api/quiz/<int:quiz_id>')
@login_required
def get_quiz_questions(quiz_id):
    """API endpoint to get quiz questions without answers"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_number).all()
    
    return jsonify({
        'quiz': {
            'id': quiz.id,
            'topic': quiz.topic,
            'difficulty': quiz.difficulty
        },
        'questions': [q.to_dict(include_answer=False) for q in questions]
    })

@quiz_bp.route('/api/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit quiz answers and get results"""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Get user answers
    data = request.get_json()
    user_answers = data.get('answers', {})
    
    # Validate that all questions are answered
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_ids = {str(q.id) for q in questions}
    answered_ids = set(user_answers.keys())
    
    if not question_ids.issubset(answered_ids):
        return jsonify({
            'success': False, 
            'message': 'Please answer all questions before submitting'
        }), 400
    
    # Calculate score and get detailed results
    score, detailed_results = calculate_quiz_score(quiz_id, user_answers)
    
    # Save result to database
    try:
        quiz_result = QuizResult(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score,
            user_answers=user_answers
        )
        db.session.add(quiz_result)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'score': score,
            'total_questions': len(questions),
            'percentage': round((score / len(questions)) * 100, 1),
            'results': detailed_results,
            'result_id': quiz_result.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to save results: {str(e)}'
        }), 500

@quiz_bp.route('/results/<int:result_id>')
@login_required
def view_results(result_id):
    """View detailed quiz results"""
    result = QuizResult.query.get_or_404(result_id)
    
    # Ensure user can only view their own results
    if result.user_id != current_user.id:
        flash('You can only view your own quiz results.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get detailed results
    score, detailed_results = calculate_quiz_score(result.quiz_id, result.user_answers)
    
    return render_template('quiz/results.html', 
                         result=result, 
                         detailed_results=detailed_results,
                         quiz=result.quiz)

@quiz_bp.route('/history')
@login_required
def quiz_history():
    """View user's quiz history"""
    results = QuizResult.query.filter_by(user_id=current_user.id)\
                             .order_by(QuizResult.taken_at.desc()).all()
    
    return render_template('quiz/history.html', results=results)
