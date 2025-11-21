import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Advanced Exam Generator", layout="centered")

# -----------------------------------------
# UPDATED QUESTION BANK WITH MARKS PER QUESTION
# -----------------------------------------
# Format:
# { subject: { topic: [ { "q": "...", "m": marks }, ... ] } }

QUESTION_BANK = {
    "Math": {
        "Algebra": [
            {"q": "Solve for x: 2x + 5 = 15.", "m": 2},
            {"q": "Factorize: x² - 9.", "m": 3},
            {"q": "Find the value of x: 3x - 7 = 11.", "m": 4},
        ],
        "Geometry": [
            {"q": "Define a right angle.", "m": 1},
            {"q": "Find the area of a circle of radius 7 cm.", "m": 5},
            {"q": "State the Pythagorean theorem.", "m": 2},
        ],
    },
    "Science": {
        "Physics": [
            {"q": "State Newton’s Second Law.", "m": 3},
            {"q": "Define velocity.", "m": 2},
            {"q": "What is the SI unit of force?", "m": 1},
        ],
        "Biology": [
            {"q": "Define photosynthesis.", "m": 3},
            {"q": "What is a cell?", "m": 2},
            {"q": "Name three plant cell organelles.", "m": 4},
        ]
    }
}

# -----------------------------------------
# TITLE
# -----------------------------------------
st.title("📘 Advanced Exam Paper Generator (Variable Marks)")
st.write("Create an exam paper with questions of different marks.")

# -----------------------------------------
# USER INPUTS
# -----------------------------------------
subject = st.selectbox("Select Subject", list(QUESTION_BANK.keys()))

topics = st.multiselect(
    "Choose Topics",
    list(QUESTION_BANK[subject].keys()),
    default=list(QUESTION_BANK[subject].keys())[:1]
)

total_marks = st.number_input("Enter Total Marks", min_value=10, max_value=300, step=5)

generate_btn = st.button("Generate Exam Paper")

# -----------------------------------------
# EXAM PAPER GENERATION
# -----------------------------------------
def generate_exam(subject, topics, total_marks):

    # Collect all questions from selected topics
    available_questions = []
    for t in topics:
        available_questions.extend(QUESTION_BANK[subject][t])

    random.shuffle(available_questions)  # randomize

    selected = []
    current_marks = 0

    # Greedy selection — pick questions until reaching closest to total_marks
    for q in available_questions:
        if current_marks + q["m"] <= total_marks:
            selected.append(q)
            current_marks += q["m"]

        # Stop if we reached the goal
        if current_marks == total_marks:
            break

    return selected, current_marks

# -----------------------------------------
# DISPLAY OUTPUT
# -----------------------------------------
if generate_btn:

    exam_questions, marks_generated = generate_exam(subject, topics, total_marks)

    if not exam_questions:
        st.error("Not enough questions to reach the required marks. Try adding more topics.")
    else:
        st.success(f"Generated Exam Paper ({marks_generated}/{total_marks} marks)")

        # Create table format
        df = pd.DataFrame({
            "Q.No": range(1, len(exam_questions) + 1),
            "Question": [q["q"] for q in exam_questions],
            "Marks": [q["m"] for q in exam_questions]
        })

        st.table(df)

        # Generate downloadable text
        text_output = f"EXAM PAPER\nSubject: {subject}\nTotal Marks: {marks_generated}\n\n"
        for idx, q in enumerate(exam_questions, 1):
            text_output += f"Q{idx}. {q['q']} ({q['m']} marks)\n"

        st.download_button(
            "Download Exam Paper (.txt)",
            text_output,
            file_name="exam_paper.txt"
        )
