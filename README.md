SAVR-AI: AI-Powered Smart Attendance System
SAVR-AI is a modern, full-stack web application designed to eliminate the daily inefficiency of manual attendance tracking in educational institutions. It leverages the power of AI-powered face recognition to create a seamless, accurate, and instantaneous attendance system from a single classroom photo and video (Though the CCTV camer).

📸 Project Showcase

Here's a look at the SAVR-AI application in action.

Teacher Dashboard

AI Detection Results

Attendance Reports







🎯 Key Features
AI-Powered Face Recognition: Uses a state-of-the-art model to detect and identify multiple students from a single classroom image.

Complete Attendance Status: Intelligently marks every student as "Present," "Absent," or flags them for "Low Confidence" manual review.

Intuitive Teacher Dashboard: A central hub providing an overview of the day's schedule and one-click access to all features.

Efficient Class Management:

Manual Enrollment: Easily add new students by taking or uploading a photo.

Bulk Import: Enroll an entire class roster in seconds using an Excel manifest and a ZIP file of photos.

Insightful Analytics: The "Attendance Reports" page features a dynamic dashboard with summary metrics, interactive charts, and a detailed data table to track trends.

Multi-Page Interface: A clean, organized, and user-friendly interface built with Streamlit's multi-page app capabilities.

⚙️ Technology Stack
Backend & Frontend: Streamlit

AI & Computer Vision:

face_recognition: For the core face detection and recognition logic.

OpenCV: For image processing and manipulation.

Pillow (PIL): For image handling.

Data Handling: Pandas

Data Visualization: Matplotlib

File Handling: PyMuPDF (fitz) for PDF processing, openpyxl for Excel.

🚀 Getting Started
Follow these instructions to set up and run the SAVR-AI project on your local machine.

Prerequisites

Python 3.9+

For macOS, you may need to install Xcode command-line tools: xcode-select --install

Installation

Clone the repository:

git clone [https://github.com/your-username/savr-ai.git](https://github.com/Harsha-Sampangi/savr-ai.git)
cd savr-ai

Create and activate a virtual environment:

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate

Install the required libraries:
A requirements.txt file is the standard way to manage dependencies. Create a file named requirements.txt with the following content:

streamlit==1.31.0
opencv-python==4.9.0.80
numpy==1.26.4
face-recognition==1.3.0
pandas==2.1.4
Pillow==10.2.0
matplotlib
openpyxl
PyMuPDF

Then, install everything with one command:

pip install -r requirements.txt

Running the Application

Once the installation is complete, run the following command in your terminal:

streamlit run app.py

Your web browser will open, and you can start using the SAVR-AI application.

📖 How to Use
Log In: Use the demo credentials to log in.

Enroll Students:

Navigate to Class Management.

Use the Bulk Import feature by uploading an Excel manifest and a ZIP file of photos.

Alternatively, enroll students one by one using the Manual Enroll form.

Take Attendance:

Navigate to the Dashboard and click "Upload Photo" or go directly to the AI Attendance Detection page.

Upload a photo of the classroom.

Click "Analyze Photo" to see the complete attendance results.

View Reports:

Go to the Attendance Reports page to see analytics and data visualizations.

⚖️ License
This project is licensed under the MIT License - see the LICENSE.md file for details.

