from app import create_app, db
from app.models import User, Message, Question
import os

app = create_app()

with app.app_context():
    try:
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Check tables
        users = User.query.all()
        print(f"Users count: {len(users)}")
        
        questions = Question.query.all()
        print(f"Questions count: {len(questions)}")
        
        messages = Message.query.all()
        print(f"Messages count: {len(messages)}")

        # Try inserting a new message to test write access
        new_msg = Message(name="Test", email="test@test.com", content="Test content")
        db.session.add(new_msg)
        db.session.commit()
        print("Successfully added a test message.")
        
        # Clean up
        db.session.delete(new_msg)
        db.session.commit()
        print("Successfully deleted test message.")

    except Exception as e:
        print(f"Error accessing DB: {e}")
        import traceback
        traceback.print_exc()
