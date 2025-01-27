from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship,declarative_base
# from sqlalchemy.orm import 

# Database URL
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/school"
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/student_management" 

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for models
Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = "students"
    name = Column(String(255), nullable=False)
    student_id = Column(Integer, primary_key=True, unique=True)
    scores = relationship("Score", back_populates="student")

# Define the Score model
class Score(Base):
    __tablename__ = "scores"
    student_id = Column(Integer, ForeignKey("students.student_id"), primary_key=True)
    subject = Column(String(255), primary_key=True)
    score = Column(Integer, nullable=False)
    student = relationship("Student", back_populates="scores")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response
class StudentCreate(BaseModel):
    name: str
    student_id: int

class StudentResponse(BaseModel):
    name: str
    student_id: int

class ScoreCreate(BaseModel):
    student_id: int
    subject: str
    score: int

class ScoreResponse(BaseModel):
    student_id: int
    subject: str
    score: int

# Initialize FastAPI app
app = FastAPI()

# CRUD operations for Students
@app.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, student_id=student.student_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/name/{name}", response_model=StudentResponse)
def read_student_by_name(name: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.name == name).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# @app.put("/students/{student_id}", response_model=StudentResponse)
# def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
#     db_student = db.query(Student).filter(Student.student_id == student_id).first()
#     if db_student is None:
#         raise HTTPException(status_code=404, detail="Student not found")
#     db_student.name = student.name
#     db_student.student_id = student.student_id
#     db.commit()
#     db.refresh(db_student)
#     return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

# API for deleting by name
@app.delete("/students/name/{name}")
def delete_student_by_name(name: str, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.name == name).first()
    # Delete correspinding score of the student as well
    db.query(Score).filter(Score.student_id == db_student.student_id).delete()

    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}


# CRUD operations for Scores
@app.post("/scores/", response_model=ScoreResponse)
def create_score(score: ScoreCreate, db: Session = Depends(get_db)):
    db_score = Score(student_id=score.student_id, subject=score.subject, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

# Add score by name
@app.post("/scores/name/{name}", response_model=ScoreResponse)
def create_score_by_name(name: str, score: ScoreCreate, db: Session = Depends(get_db)):    
    db_student = db.query(Student).filter(Student.name == name).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found! First add the student")
    db_score = Score(student_id=db_student.student_id, subject=score.subject, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@app.get("/scores/{student_id}/{subject}", response_model=ScoreResponse)
def read_score(student_id: int, subject: str, db: Session = Depends(get_db)):
    score = db.query(Score).filter(Score.student_id == student_id, Score.subject == subject).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return score

@app.put("/scores/{student_id}/{subject}", response_model=ScoreResponse)
def update_score(student_id: int, subject: str, score: ScoreCreate, db: Session = Depends(get_db)):
    db_score = db.query(Score).filter(Score.student_id == student_id, Score.subject == subject).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db_score.student_id = score.student_id
    db_score.subject = score.subject
    db_score.score = score.score
    db.commit()
    db.refresh(db_score)
    return db_score

@app.delete("/scores/{student_id}/{subject}")
def delete_score(student_id: int, subject: str, db: Session = Depends(get_db)):
    db_score = db.query(Score).filter(Score.student_id == student_id, Score.subject == subject).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(db_score)
    db.commit()
    return {"message": "Score deleted successfully"}

# API endpoints for summarizing the a students marks
@app.get("/summarize_by_student_id/{student_id}")
def summarize_marks_by_student_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    scores = db.query(Score).filter(Score.student_id == student_id).all()
    total_marks = sum(score.score for score in scores)
    percentage = (total_marks / (100 *len(scores)) * 100)
    return {"name": student.name, "student_id": student.student_id, "total_marks": total_marks, "percentage": percentage}

@app.get("/summarize_by_student_name/{student_name}")
def summarize_marks(student_name: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.name == student_name).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    scores = db.query(Score).filter(Score.student_id == student.student_id).all()
    total_marks = sum(score.score for score in scores)
    percentage = (total_marks / (100 *len(scores)) * 100)
    return {"name": student.name, "student_id": student.student_id, "total_marks": total_marks, "percentage": percentage}

# API endpoint for summarizing the marks by subject
@app.get("/summarize_by_subject/{subject}")
def summarize_marks_by_subject(subject: str, db: Session = Depends(get_db)):
    scores = db.query(Score).filter(Score.subject == subject).all()
    total_marks = sum(score.score for score in scores)
    # calculate the average marks
    percentage = (total_marks / (100 *len(scores)) * 100)
    # percentage = (total_marks / 500) * 100
    return {"subject": subject, "total_marks": total_marks, "percentage": percentage}