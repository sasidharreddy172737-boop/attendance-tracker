# 📚 Attendance Tracker

A personal attendance tracking web app built with Python and Streamlit.
Helps students track semester-wise attendance and predicts how many 
classes can be skipped or must be attended to maintain 75% attendance.

## Live Demo
[Click Here]https://attendance-tracker-9kvdpwteycvnng8e3wmhgv.streamlit.app/

## Features
- Semester-wise subject organization
- Daily attendance marking (Present / Absent / No Class)
- Live attendance percentage calculation
- Predicts how many classes can be safely skipped
- Predicts how many classes must be attended if behind
- Overall semester attendance summary
- Data persists across sessions

## How It Works
1. Select or add a semester
2. Add subjects with total planned classes
3. Mark daily attendance for each subject
4. View live percentage and recommendations

## Tech Stack
- Python
- Streamlit
- JSON (for data storage)
- Object-Oriented Programming (Subject, Semester, Attendance classes)

## How to Run Locally
\`\`\`bash
pip install -r requirements.txt
streamlit run main.py
\`\`\`

## What I Learned Building This
- Applying OOPs concepts to a real-world problem
- Building a full working app with Streamlit
- Managing state with Streamlit's session_state
- JSON-based data persistence
- Deploying a Python app to the cloud
