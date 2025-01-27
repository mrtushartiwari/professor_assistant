from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import random

# Define the database connection URL
# Replace with your actual database credentials
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/student_management" 

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Base class for declarative class definitions
Base = declarative_base()

# Define the 'students' table
class Student(Base):
    __tablename__ = 'students'
    
    name = Column(String(255))
    student_id = Column(Integer, primary_key=True, unique=True)
    
    # Relationship to the 'scores' table
    scores = relationship('Score', back_populates='student')

# Define the 'scores' table
class Score(Base):
    __tablename__ = 'scores'
    
    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    subject = Column(String(255), primary_key=True)
    score = Column(Integer)
    
    # Relationship to the 'students' table
    student = relationship('Student', back_populates='scores')

# Create all tables in the database
Base.metadata.create_all(engine)

print("Tables 'students' and 'scores' created successfully.")



## Add 10 students

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# List of students to insert
students_data = [
    {"name": "Alice", "student_id": 1},
    {"name": "Bob", "student_id": 2},
    {"name": "Charlie", "student_id": 3},
    {"name": "David", "student_id": 4},
    {"name": "Eve", "student_id": 5},
    {"name": "Frank", "student_id": 6},
    {"name": "Grace", "student_id": 7},
    {"name": "Hank", "student_id": 8},
    {"name": "Ivy", "student_id": 9},
    {"name": "Jack", "student_id": 10},
]

try:
    # Insert students into the 'students' table
    for student in students_data:
        new_student = Student(name=student["name"], student_id=student["student_id"])
        session.add(new_student)
    
    # Commit the transaction
    session.commit()
    print("10 students inserted successfully.")

except Exception as e:
    # Rollback in case of error
    session.rollback()
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.close()



## Adding subjects

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# List of subjects
subjects = ["Physics", "Chemistry", "Maths", "Computer Science", "English"]

try:
    # Fetch all students from the 'students' table
    students = session.query(Student).all()

    # Insert scores for each student
    for student in students:
        for subject in subjects:
            # Generate a random score between 0 and 100
            random_score = random.randint(30, 100)
            
            # Create a new score record
            new_score = Score(student_id=student.student_id, subject=subject, score=random_score)
            session.add(new_score)
    
    # Commit the transaction
    session.commit()
    print("Scores inserted successfully for all students.")

except Exception as e:
    # Rollback in case of error
    session.rollback()
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.close()