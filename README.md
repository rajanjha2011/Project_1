# Project_1 Placement Eligibity Streamlit App
Placement Eligibility Streamlit Application
Student Placement Eligibility App
This is a beginner-friendly Streamlit web application that helps HR professionals or placement officers filter eligible students for placement based on performance data. It uses fake student data generated with the Faker library and stores it in a MySQL database with interrelated tables.

Features
 Login system for basic admin access

 Generates synthetic student data (30 students) using Faker

 Stores data in 4 linked MySQL tables:

Students (personal info)

Programming (coding stats)

SoftSkills (communication, teamwork, etc.)

Placement (interview and job details)

 Allows filtering students based on:

Mock interview scores

CodeKata problems solved

Mini/final projects completed

Project scores

Programming language
Displays eligible students in a clean table using SQL JOINs

 Tech Stack
Frontend: Streamlit
Backend: MySQL
Data Generator: Faker
Language: Python

 How to Run
Install requirements
pip install streamlit mysql-connector-python faker pandas
Start your MySQL server (with user root and password yourpassword)

Run the app:
streamlit run ds_placement_app.py

Login with:
Username: admin
Password: 1234
Click "Generate Sample Data" to create the database and fill tables

 Use Case
This app is useful for:

Educational institutions managing placement drives

Beginner data scientists learning Streamlit + SQL + Python

HR filtering systems in internal tools or dashboards

