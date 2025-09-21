# 1. IMPORTS
import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
from datetime import datetime
from PIL import Image
import zipfile
import io
import matplotlib.pyplot as plt  # Import for creating charts

# 2. CONFIGURATION AND SETUP
DATASET_PATH = "dataset"
REPORTS_PATH = "attendance_reports"

# 3. HELPER FUNCTIONS
def ensure_dirs():
    """Create necessary directories if they don't exist."""
    os.makedirs(DATASET_PATH, exist_ok=True)
    os.makedirs(REPORTS_PATH, exist_ok=True)

def load_known_faces():
    """Loads all known faces from the dataset directory."""
    known_face_encodings = []
    known_faces_data = []  # Will store {"roll": ..., "name": ...}
    
    if not os.path.exists(DATASET_PATH) or not os.listdir(DATASET_PATH):
        return [], []
        
    for filename in os.listdir(DATASET_PATH):
        if filename.endswith((".jpg", ".png")):
            path = os.path.join(DATASET_PATH, filename)
            name_part = os.path.splitext(filename)[0]
            
            try:
                roll, name = name_part.split(" - ", 1)
            except ValueError:
                st.toast(f"Skipping invalid filename: {filename}", icon="⚠️")
                continue

            try:
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_faces_data.append({"roll": roll.strip(), "name": name.strip()})
            except Exception as e:
                st.toast(f"Error processing {filename}: {e}", icon="⚠️")
    
    return known_face_encodings, known_faces_data

# --- MOCK DATA FOR UI ---
mock_schedule = [
    {"id": "CS-301", "name": "Data Structures", "time": "9:00 AM", "status": "completed", "attended": 45, "total": 50},
    {"id": "CS-205", "name": "Algorithms", "time": "11:00 AM", "status": "completed", "attended": 38, "total": 42},
    {"id": "CS-401", "name": "Machine Learning", "time": "2:00 PM", "status": "upcoming"},
    {"id": "CS-302", "name": "Database Systems", "time": "4:00 PM", "status": "upcoming"},
]

# 4. PAGE RENDERING FUNCTIONS

def render_login_page():
    """Renders the login form for the application."""
    st.title("Savr Attend")
    st.caption("AI-Powered Attendance Management")

    with st.form("login_form"):
        st.subheader("Welcome Back")
        email = st.text_input("Email", value="teacher@demo.com")
        password = st.text_input("Password", type="password", value="demo123")
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

        if submitted:
            st.session_state.logged_in = True
            st.rerun()

def render_dashboard():
    """Renders the main teacher dashboard."""
    st.title("Teacher Dashboard")
    st.caption("Welcome back, Harsha Sampangi")
    
    st.divider()

    # --- Updated Action Cards ---
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.image("https://i.imgur.com/2s9EM8A.png", width=64) # Camera Icon
            st.subheader("Take Attendance")
            st.write("Upload a classroom photo and let AI detect students automatically.")
            if st.button("Upload Photo", key="dash_upload", use_container_width=True, type="primary"):
                st.session_state.page = "take_attendance"
                st.rerun()
    with col2:
        with st.container(border=True):
            st.image("https://i.imgur.com/J222sV1.png", width=64) # Reports Icon
            st.subheader("Attendance Reports")
            st.write("View detailed attendance reports and export data.")
            if st.button("View Reports", key="dash_reports", use_container_width=True):
                st.session_state.page = "reports"
                st.rerun()
    with col3:
        with st.container(border=True):
            st.image("https://i.imgur.com/K9w282v.png", width=64) # Class Mgmt Icon
            st.subheader("Class Management")
            st.write("Manage your classes and student information.")
            if st.button("Manage Classes", key="dash_mgmt", use_container_width=True):
                st.session_state.page = "class_management"
                st.rerun()
    
    st.divider()
    
    # Mock schedule data
    mock_schedule = [
        {"id": "CS-301", "name": "Data Structures", "time": "09:00 AM - 10:00 AM", "status": "completed", "attended": 25, "total": 30},
        {"id": "CS-205", "name": "Algorithms", "time": "11:00 AM - 12:00 PM", "status": "upcoming", "attended": 0, "total": 30},
        {"id": "CS-404", "name": "Operating Systems", "time": "01:00 PM - 02:00 PM", "status": "upcoming", "attended": 0, "total": 30},
    ]

    st.subheader("Today's Classes")
    for cls in mock_schedule:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{cls['id']} - {cls['name']}**")
                st.caption(cls['time'])
            with col2:
                if cls['status'] == "completed":
                    st.markdown(f"**{cls['attended']}/{cls['total']}** attended")
                else:
                    st.markdown(f"**Upcoming**")
            with col3:
                if cls['status'] == "completed":
                    st.button("View Report", key=f"report_{cls['id']}", use_container_width=True)
                else:
                    st.button("Start Now", key=f"start_{cls['id']}", use_container_width=True, type="primary")

def render_take_attendance_page():
    """Renders the AI Attendance Detection page."""
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.title("AI Attendance Detection")
    st.caption("Upload a clear photo of your classroom.")

    if not st.session_state.known_faces_data:
        st.warning("No students enrolled. Please add students in 'Class Management'.")
        return

    uploaded_file = st.file_uploader("Choose a classroom photo", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        if st.button("🔍 Analyze Photo", use_container_width=True, type="primary"):
            with st.spinner("Analyzing image... This may take a moment."):
                image = Image.open(uploaded_file)
                frame = np.array(image)
                
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                
                results = []
                for face_encoding in face_encodings:
                    face_distances = face_recognition.face_distance(st.session_state.known_face_encodings, face_encoding)
                    if face_distances.size > 0:
                        best_match_index = np.argmin(face_distances)
                        distance = face_distances[best_match_index]
                        confidence = (1 - distance) * 100
                        student_data = st.session_state.known_faces_data[best_match_index]
                        
                        if not any(r['roll'] == student_data['roll'] for r in results):
                            results.append({
                                "name": student_data['name'], 
                                "roll": student_data['roll'],
                                "confidence": confidence
                            })
                
                detected_rolls = {r['roll'] for r in results}
                all_known_rolls = {student['roll'] for student in st.session_state.known_faces_data}
                absent_rolls = all_known_rolls - detected_rolls

                for roll in sorted(list(absent_rolls)):
                    student_data = next(item for item in st.session_state.known_faces_data if item["roll"] == roll)
                    results.append({"name": student_data['name'], "roll": roll, "confidence": -1})
                
                st.session_state.analysis_results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        
        if "analysis_results" in st.session_state and st.session_state.analysis_results is not None:
            with st.container(border=True):
                results = st.session_state.analysis_results
                present_count = sum(1 for r in results if r['confidence'] > 75)
                review_count = sum(1 for r in results if 0 <= r['confidence'] <= 75)
                absent_count = sum(1 for r in results if r['confidence'] < 0)
                
                # Header Section
                col1, col2, col3 = st.columns([5, 2, 2])
                with col1:
                    st.markdown(f"**Detection Results**")
                    st.caption(f"Found {present_count} present, {absent_count} absent, {review_count} needs review.")
                with col2:
                    st.button("Save & Continue", use_container_width=True)
                with col3:
                    if st.button("Mark Attendance Now", use_container_width=True, type="primary"):
                        st.success("Attendance has been marked!")

                st.divider()

                # Results Grid
                num_columns = 3
                cols = st.columns(num_columns)
                for i, result in enumerate(results):
                    with cols[i % num_columns]:
                        with st.container(border=True, height=180):
                            st.markdown(f"**{result['name']}** <span style='float:right; color:grey; font-size: 0.9em;'>{result['roll']}</span>", unsafe_allow_html=True)
                            
                            col_status, col_value = st.columns(2)
                            with col_status:
                                st.caption("Status:")
                                st.caption("Confidence:")
                            
                            with col_value:
                                if result['confidence'] > 75:
                                    st.markdown(f"<div style='text-align: right; color: green;'><b>✅ Present</b><br>{result['confidence']:.0f}%</div>", unsafe_allow_html=True)
                                elif result['confidence'] >= 0:
                                    st.markdown(f"<div style='text-align: right; color: orange;'><b>⚠️ Low Confidence</b><br>{result['confidence']:.0f}%</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div style='text-align: right; color: red;'><b>❌ Absent</b><br>0%</div>", unsafe_allow_html=True)
                            
                            if 0 <= result['confidence'] <= 75:
                                st.button("Manual Review", key=f"review_{result['roll']}", use_container_width=True)


def render_reports_page():
    """Renders the Attendance Reports page with charts and detailed table."""
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("Attendance Reports")
    st.caption("View and analyze attendance patterns.")

    # --- Filters and Export Buttons ---
    col1, col2, col3, col4 = st.columns([2,2,1,1])
    with col1:
        st.selectbox("Filter by Class", ["CS-301 Data Structures", "CS-205 Algorithms"])
    with col2:
        st.selectbox("Filter by Time", ["This Week", "This Month", "All Time"])
    with col3:
        st.download_button("Export CSV", "name,roll,status\nAlice,CS001,Present", "attendance.csv", use_container_width=True)
    with col4:
        st.button("Export PDF", use_container_width=True) # PDF export is more complex, so this is a placeholder

    st.divider()

    # --- Summary Metrics ---
    total_students = 8
    present_students = 6
    review_needed = 2
    attendance_rate = (present_students / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Students", f"{total_students}")
    with col2:
        st.metric("✅ Present", f"{present_students}")
    with col3:
        st.metric("⚠️ Need Review", f"{review_needed}")
    with col4:
        st.metric("📈 Attendance Rate", f"{attendance_rate:.0f}%")

    st.divider()

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Today's Attendance")
        
        # Data for Donut Chart
        labels = 'Present', 'Absent', 'Low Confidence'
        sizes = [6, 1, 2] # Mock data
        colors = ['#22c55e', '#ef4444', '#f97316']
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
               wedgeprops=dict(width=0.4, edgecolor='w'))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

    with col2:
        st.subheader("Weekly Trend")
        # Data for Bar Chart
        chart_data = pd.DataFrame({
           "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"],
           "Attendance %": [88, 92, 85, 95, 94, 89, 75] # Mock data
        })
        st.bar_chart(chart_data.set_index("Day"))

    st.divider()

    # --- Detailed Record Table ---
    st.subheader("Detailed Attendance Record")
    mock_report_data = {
        "Name": ["Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Eva Brown", "Frank Miller", "Grace Taylor", "Henry Anderson"],
        "Roll No": ["CS001", "CS002", "CS003", "CS004", "CS005", "CS006", "CS007", "CS008"],
        "Status": ["Present", "Present", "Present", "Review", "Present", "Absent", "Present", "Review"],
        "Confidence": ["95%", "88%", "92%", "67%", "94%", "0%", "89%", "73%"],
        "Last Seen": ["2025-09-14 09:00", "2025-09-14 09:00", "2025-09-14 09:00", "2025-09-14 09:00", "2025-09-14 09:00", "2025-09-12 09:00", "2025-09-14 09:00", "2025-09-14 09:00"]
    }
    df = pd.DataFrame(mock_report_data)
    st.dataframe(df, use_container_width=True)


def render_class_management_page():
    """Renders the Class Management page with Excel import."""
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.title("Class Management")
    st.caption("Manage your enrolled students.")

    # --- BULK IMPORT SECTION ---
    with st.expander("⬇️ Bulk Import Students from Excel"):
        st.info("Upload an Excel manifest and a ZIP file with all corresponding student photos.")
        
        excel_file = st.file_uploader("Upload Student Manifest (.xlsx)", type=["xlsx"])
        zip_file = st.file_uploader("Upload Photos ZIP File", type="zip")

        if st.button("Process Bulk Import", use_container_width=True):
            if excel_file and zip_file:
                with st.spinner("Processing files..."):
                    try:
                        df = pd.read_excel(excel_file)
                        required_columns = ["ROLL NO", "NAME", "PHOTO"]
                        if not all(col in df.columns for col in required_columns):
                            st.error(f"Excel file must contain the columns: {', '.join(required_columns)}")
                            return

                        student_manifest = df.to_dict('records')
                        st.info(f"Found {len(student_manifest)} students in Excel. Processing images...")

                        zip_archive = zipfile.ZipFile(io.BytesIO(zip_file.read()))
                        image_filenames_in_zip = zip_archive.namelist()
                        
                        success_count, fail_count = 0, 0
                        for student in student_manifest:
                            photo_filename = str(student['PHOTO'])
                            photo_found = False
                            for zip_filename in image_filenames_in_zip:
                                if zip_filename.endswith(photo_filename):
                                    new_filename = f"{student['ROLL NO']} - {student['NAME']}.jpg"
                                    filepath = os.path.join(DATASET_PATH, new_filename)
                                    with zip_archive.open(zip_filename) as image_file, open(filepath, "wb") as f:
                                        f.write(image_file.read())
                                    success_count += 1
                                    photo_found = True
                                    break
                            
                            if not photo_found:
                                st.warning(f"Photo '{photo_filename}' for {student['NAME']} not found in ZIP.")
                                fail_count += 1
                        
                        st.success(f"Import complete! Enrolled {success_count} students.")
                        if fail_count > 0:
                            st.error(f"Failed to find photos for {fail_count} students.")
                        
                        st.session_state.known_face_encodings, st.session_state.known_faces_data = load_known_faces()
                        st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred during bulk import: {e}")
            else:
                st.error("Please upload both an Excel and a ZIP file.")

    st.divider()

    # --- MANUAL ENROLL SECTION ---
    st.subheader("Enroll New Student (Manual)")
    with st.form("enroll_form"):
        student_name = st.text_input("Student Name", placeholder="e.g., Ada Lovelace")
        student_roll = st.text_input("Student Roll Number", placeholder="e.g., CS001")
        
        tab1, tab2 = st.tabs(["Take Photo with Camera", "Upload Photo from Device"])
        img_file_buffer = None
        uploaded_image = None
        
        with tab1:
            img_file_buffer = st.camera_input("Take Picture")
        with tab2:
            uploaded_image = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])
            
        submitted = st.form_submit_button("Enroll Student", use_container_width=True)

        if submitted and student_name and student_roll:
            image_bytes = None
            if img_file_buffer is not None:
                image_bytes = img_file_buffer.getvalue()
            elif uploaded_image is not None:
                image_bytes = uploaded_image.getvalue()

            if image_bytes:
                cv2_img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                face_locations = face_recognition.face_locations(cv2_img)
                
                if len(face_locations) == 1:
                    filename = f"{student_roll} - {student_name}.jpg"
                    filepath = os.path.join(DATASET_PATH, filename)
                    cv2.imwrite(filepath, cv2_img)
                    st.success(f"Successfully enrolled {student_name} ({student_roll})!")
                    st.session_state.known_face_encodings, st.session_state.known_faces_data = load_known_faces()
                else:
                    st.error("Could not enroll. Ensure one clear face is in the picture.")
            else:
                st.error("Please take or upload a photo to enroll the student.")

    st.divider()
    
    # --- ENROLLED STUDENTS LIST ---
    st.subheader("Enrolled Students")
    if not st.session_state.known_faces_data:
        st.info("No students enrolled yet.")
    else:
        for student in st.session_state.known_faces_data:
            st.markdown(f"- **{student['roll']}**: {student['name']}")

# 5. MAIN APPLICATION LOGIC
def main():
    """The main function that runs the Streamlit app."""
    st.set_page_config(page_title="SAVR Attend", layout="wide")
    ensure_dirs()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "known_faces_data" not in st.session_state:
        st.session_state.known_face_encodings, st.session_state.known_faces_data = load_known_faces()

    if not st.session_state.logged_in:
        render_login_page()
    else:
        # The main router that displays the correct page
        pages = {
            "dashboard": render_dashboard,
            "take_attendance": render_take_attendance_page,
            "reports": render_reports_page,
            "class_management": render_class_management_page,
        }
        
        # --- NEW: Sidebar removed, header is now inside each page ---
        # The routing logic will call the appropriate page function
        render_func = pages.get(st.session_state.page, render_dashboard)
        render_func()

if __name__ == "__main__":
    main()

