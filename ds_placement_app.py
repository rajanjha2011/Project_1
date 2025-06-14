import streamlit as st
import mysql.connector
from faker import Faker
import random
import pandas as pd

# Page Setup

st.set_page_config(page_title="Placement App")
st.title("Student Placement Eligibility App")

# Set up the credentials to access the app

st.sidebar.header("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if username != "admin" or password != "1234":
    st.warning("Please enter correct login details.")
    st.stop()

# Connect to MySQL

@st.cache_resource(show_spinner=False)
def connect_database():

    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rajan@6319",
        connection_timeout = 5    # 5 seconds timeout 
        )
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS placement_db")
        cur.execute("USE placement_db")
        return conn, cur
    except mysql.connector.Error as e:
        st.error(f"Failed to connect to MySQL: {e}")
        st.stop()

conn, cursor = connect_database()

# Create Database

def create_tables():
    cursor.execute("DROP TABLE IF EXISTS Placement")
    cursor.execute("DROP TABLE IF EXISTS SoftSkills")
    cursor.execute("DROP TABLE IF EXISTS Programming")
    cursor.execute("DROP TABLE IF EXISTS Students")
   
    cursor.execute("""
        CREATE TABLE Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100), age INT, gender VARCHAR(10),
            email VARCHAR(100), phone VARCHAR(20),
            enrollment_year INT, course_batch VARCHAR(50),
            city VARCHAR(50), graduation_year INT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Programming (
            programming_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT, language VARCHAR(50),
            problems_solved INT, mini_projects INT,
            final_projects INT, final_project_score FLOAT,
            average_project_score FLOAT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE SoftSkills (
            soft_skill_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            communication INT, teamwork INT,
            presentation INT, leadership INT,
            critical_thinking INT, interpersonal_skills INT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Placement (
            placement_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT, mock_interview_score INT,
            internships_completed INT, placement_status VARCHAR(50),
            company_name VARCHAR(100), placement_package FLOAT,
            interview_rounds_cleared INT, placement_date DATE,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    """)
    conn.commit()

create_tables()

# Using Faker library
def insert_fake_data():
    fake = Faker()
    for _ in range(20):  # Generate 20 fake students
        name = fake.name()
        age = random.randint(20, 25)
        gender = random.choice(["Male", "Female"])
        email = fake.email()
        phone = fake.phone_number()[:20]
        enroll = random.randint(2019, 2022)
        batch = f"Batch-{random.randint(1,3)}"
        city = fake.city()
        grad = enroll + 4
        
        # Insert into Students
        cursor.execute("""
            INSERT INTO Students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (name, age, gender, email, phone, enroll, batch, city, grad))
        student_id = cursor.lastrowid
        
        # Programming info
        lang = random.choice(["Python", "Java", "C++", "SQL"])
        problems = random.randint(50, 200)
        mini = random.randint(1, 3)
        final = random.randint(1, 2)
        final_score = random.uniform(60, 100)
        avg_score = (final_score + random.uniform(50, 100)) / 2

        cursor.execute("""
            INSERT INTO Programming (student_id, language, problems_solved, mini_projects, final_projects, final_project_score, average_project_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (student_id, lang, problems, mini, final, final_score, avg_score))

        # Soft skills
        cursor.execute("""
            INSERT INTO SoftSkills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (student_id,
              random.randint(50, 100), random.randint(50, 100), random.randint(50, 100),
              random.randint(50, 100), random.randint(50, 100), random.randint(50, 100)))
        
        # Placement info
        status = random.choice(["Placed", "Ready", "Not Ready"])
        company = fake.company() if status == "Placed" else None
        package = random.uniform(3.0, 10.0) if status == "Placed" else None
        rounds = random.randint(1, 5)
        date = fake.date_between(start_date="-1y", end_date="today") if status == "Placed" else None

        cursor.execute("""
            INSERT INTO Placement (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (student_id, random.randint(1, 10), random.randint(0, 2), status, company, package, rounds, date))

    conn.commit()

# Add button to run manually

with st.expander(" Setup Database and Insert Sample Data (Run Only Once)"):
    if st.button("Generate Fake Student Data"):
        create_tables()
        insert_fake_data()
        st.success("Database Created and sample data  inserted successfully.")


# Filters for eligibility check

st.header("Filter Eligible Students")

mock_min = st.slider("Mock Interview Score", 0, 10, 5)
kata_min = st.slider("Minimum CodeKata Problems", 0, 200, 50)
mini_min = st.slider("Mini Projects Completed", 0, 5, 1)
final_min = st.slider("Final Projects Completed", 0, 5, 1)
score_min = st.slider("Minimum Final Project Score", 0, 100, 60)
avg_min = st.slider("Minimum Average Score", 0, 100, 70)
lang = st.selectbox("Programming Language", ["All", "Python", "Java", "C++", "SQL"])

# Run SQL Query

query = """
    SELECT s.name, s.email, p.language, p.problems_solved,
           p.mini_projects, p.final_projects, p.final_project_score,
           p.average_project_score, pl.mock_interview_score, pl.placement_status
    FROM Students as s
    JOIN Programming as p ON s.student_id = p.student_id
    JOIN Placement as pl ON s.student_id = pl.student_id
    WHERE pl.mock_interview_score >= %s
      AND p.problems_solved >= %s
      AND p.mini_projects >= %s
      AND p.final_projects >= %s
      AND p.final_project_score >= %s
      AND p.average_project_score >= %s
"""

params = [mock_min, kata_min, mini_min, final_min, score_min, avg_min]

if lang != "All":
    query += " AND p.language = %s"
    params.append(lang)

cursor.execute(query, params)
results = cursor.fetchall()

# Show Results

if results:
    df = pd.DataFrame(results, columns=[
        "Name", "Email", "Language", "CodeKata", "Mini Projects",
        "Final Projects", "Final Score", "Average Score", "Mock Interview Score", "Status"
    ])
    st.success(f" Found {len(df)} matching students")
    st.dataframe(df)
else:
    st.warning("No students found for the selected criteria.")
