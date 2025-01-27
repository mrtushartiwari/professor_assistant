from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Define the database connection URL
# Replace with your actual database credentials
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/student_management" 

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing tables
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the table objects
students_table = Table('students', metadata, autoload_with=engine)
scores_table = Table('scores', metadata, autoload_with=engine)

try:
    # Delete all rows from the 'scores' table
    session.execute(scores_table.delete())
    print("All rows deleted from 'scores' table.")

    # Delete all rows from the 'students' table
    session.execute(students_table.delete())
    print("All rows deleted from 'students' table.")

    # Commit the transaction
    session.commit()

except Exception as e:
    # Rollback in case of error
    session.rollback()
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.close()