SAVR Attend - AI-Powered Attendance System
SAVR Attend is a smart, AI-driven attendance management system built with Python and Streamlit. It leverages real-time face recognition to automate the tedious process of taking attendance, providing a seamless experience for both teachers and students through an intuitive web interface.

✨ Key Features
👤 Dual User Dashboards: Separate, secure login and dashboard views for Teachers and Students.

📸 Photo-Based Attendance: Teachers can upload a single classroom photo, and the system automatically detects and marks all recognized students.

🎥 Live CCTV Monitoring: Monitor attendance in real-time using a live feed from a CCTV camera (via RTSP URL) or a standard webcam.

🤔 Manual Review System: For low-confidence matches, the system prompts the teacher to manually confirm a student's status (Present or Absent), ensuring 100% accuracy.

⬆️ Bulk Student Enrollment: Easily enroll an entire class by uploading an Excel file with student details and a ZIP file with their photos.

📊 Dynamic Reporting: All attendance sessions are saved as CSV files. The reports page allows teachers to load, view, and analyze past attendance records with visual charts.

🖼️ Visual Feedback: Both photo and CCTV modes provide visual feedback by drawing bounding boxes around detected faces (Green for recognized, Red for unknown).

🛠️ Technology Stack
Backend: Python

Web Framework: Streamlit

Face Recognition: face_recognition (built on dlib)

Image Processing: OpenCV, Pillow

Data Handling: Pandas, NumPy

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

1. Prerequisites

Python 3.9 or higher

pip for package management

2. Installation

Clone the repository:

git clone [https://github.com/Harsha-Sampangi/SAVR-AI.git](https://github.com/Harsha-Sampangi/SAVR-AI.git)
cd SAVR-AI

Create and activate a virtual environment:

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate

Install the required dependencies:
The project is organized within the savr_ai folder. Install requirements from there:

pip install -r savr_ai/requirements.txt

3. Setup

Create Data Folders: Before running the app, ensure the dataset and attendance_reports folders exist in the root directory (SAVR-AI/).

Enroll Students: Add student images to the SAVR-AI/dataset/ folder. The filename for each image must be in the format: ROLL_NUMBER - NAME.jpg.

Example: CS001 - Alice Johnson.jpg

4. Running the Application

Navigate to the root project directory (SAVR-AI/) and run the Streamlit app:

streamlit run savr_ai/app.py

The application will open in your default web browser.

📖 How to Use
Login: Use the demo credentials to log in as a Teacher or Student.

Teacher: teacher@demo.com / demo123

Student: student@demo.com / demo123

Manage Classes: Use the "Class Management" page to enroll new students manually or in bulk.

Take Attendance:

Navigate to "Take Attendance," upload a class photo, and click "Analyze."

Review the results, correct any low-confidence matches, and click "Save & Continue."

CCTV Monitoring:

Go to the "CCTV Monitoring" page and click "Start Monitoring."

Click "Stop Monitoring" to end the session.

Review the detected students and save the report.

View Reports: On the "Reports" page, select a saved CSV file from the dropdown to view detailed attendance data and visualizations.

📄 License
This project is licensed under the MIT License. See the LICENSE.md file for details.
