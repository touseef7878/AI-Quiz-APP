import json
import google.generativeai as genai
from flask import current_app
from models import Quiz, Question, db

class AIQuizGenerator:
    def __init__(self):
        self.client = None
        if current_app.config.get('GEMINI_API_KEY'):
            genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
            self.client = genai
    
    def generate_quiz_prompt(self, topic, difficulty):
        difficulty_descriptions = {
            'simple': 'basic level questions suitable for beginners',
            'medium': 'intermediate level questions with moderate complexity',
            'hard': 'advanced level questions requiring deep understanding'
        }
        
        prompt = f"""Generate exactly 10 multiple-choice questions about "{topic}" at {difficulty_descriptions[difficulty]} level.

Requirements:
1. Each question must have exactly 4 options (A, B, C, D)
2. Only one option should be correct
3. Include a brief explanation (2-3 sentences) for each correct answer
4. Questions should be diverse and cover different aspects of the topic
5. Avoid overly tricky or ambiguous questions

Format your response as a JSON array with this exact structure:
[
  {{
    "question_number": 1,
    "question_text": "Your question here?",
    "option_a": "First option",
    "option_b": "Second option", 
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_option": "A",
    "explanation": "Brief explanation why this answer is correct."
  }}
]

Topic: {topic}
Difficulty: {difficulty}
Number of questions: 10"""
        
        return prompt
    
    def parse_ai_response(self, response_text):
        """Parse AI response and extract questions"""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            questions_data = json.loads(json_str)
            
            # Validate the structure
            if not isinstance(questions_data, list) or len(questions_data) != 10:
                raise ValueError("Response must contain exactly 10 questions")
            
            for i, q in enumerate(questions_data):
                required_fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'explanation']
                for field in required_fields:
                    if field not in q:
                        raise ValueError(f"Missing field '{field}' in question {i+1}")
                
                if q['correct_option'] not in ['A', 'B', 'C', 'D']:
                    raise ValueError(f"Invalid correct_option '{q['correct_option']}' in question {i+1}")
            
            return questions_data
            
        except (json.JSONDecodeError, ValueError) as e:
            current_app.logger.error(f"Failed to parse AI response: {e}")
            return None
    
    def generate_quiz(self, topic, difficulty):
        """Generate a complete quiz with AI"""
        try:
            if not self.client:
                return self._generate_fallback_quiz(topic, difficulty)
            
            prompt = self.generate_quiz_prompt(topic, difficulty)
            
            # Call Gemini API
            model = self.client.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            response_text = response.text
            questions_data = self.parse_ai_response(response_text)
            
            if not questions_data:
                return self._generate_fallback_quiz(topic, difficulty)
            
            # Create quiz in database
            quiz = Quiz(topic=topic, difficulty=difficulty)
            db.session.add(quiz)
            db.session.flush()  # Get the quiz ID
            
            # Create questions
            for i, q_data in enumerate(questions_data, 1):
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q_data['question_text'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_option=q_data['correct_option'],
                    explanation=q_data['explanation'],
                    question_number=i
                )
                db.session.add(question)
            
            db.session.commit()
            return quiz
            
        except Exception as e:
            current_app.logger.error(f"AI quiz generation failed: {e}")
            db.session.rollback()
            return self._generate_fallback_quiz(topic, difficulty)
    
    def _generate_fallback_quiz(self, topic, difficulty):
        """Generate a fallback quiz when AI is unavailable"""
        # Create a sample quiz for demonstration
        quiz = Quiz(topic=topic, difficulty=difficulty)
        db.session.add(quiz)
        db.session.flush()
        
        # Sample questions - in production, you'd want a better fallback
        sample_questions = [
            {
                "question_text": f"This is a sample {difficulty} question about {topic}. What is the main concept?",
                "option_a": "Concept A",
                "option_b": "Concept B", 
                "option_c": "Concept C",
                "option_d": "Concept D",
                "correct_option": "A",
                "explanation": f"This is a sample explanation for {topic} at {difficulty} level."
            }
        ] * quiz_questions_count
        
        for i, q_data in enumerate(sample_questions, 1):
            q_data["question_text"] = f"Question {i}: {q_data['question_text']}"
            question = Question(
                quiz_id=quiz.id,
                question_text=q_data['question_text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_option=q_data['correct_option'],
                explanation=q_data['explanation'],
                question_number=i
            )
            db.session.add(question)
        
        db.session.commit()
        return quiz

def calculate_quiz_score(quiz_id, user_answers):
    """Calculate score and return detailed results"""
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.question_number).all()
    
    score = 0
    results = []
    
    for question in questions:
        user_answer = user_answers.get(str(question.id))
        is_correct = user_answer == question.correct_option
        
        if is_correct:
            score += 1
        
        results.append({
            'question_number': question.question_number,
            'question_text': question.question_text,
            'options': {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d
            },
            'user_answer': user_answer,
            'correct_answer': question.correct_option,
            'is_correct': is_correct,
            'explanation': question.explanation
        })
    
    return score, results