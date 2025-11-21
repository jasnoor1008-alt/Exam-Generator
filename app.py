import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Exam Paper Generator", layout="centered")

# ------------------------------
# SAMPLE QUESTION BANK TEMPLATE
# ------------------------------
# You can replace this with your own CSV or DB
QUESTION_BANK = {
    "Math": {
        "Algebra": [
            "Solve for x: 2x + 5 = 15.",
            "Factorize: x² - 9.",
            "Find the value of x: 3x - 7 = 11."
        ],
        "Geometry": [
            "What is the sum of interior angles of a pentagon?",
            "Define a right-angled triangle.",
            "Find the area of a circle with radius 7cm."
        ]
    },
    "Science": {
        "Physics": [
            "State Newton’s Second Law.",
            "Define velocity.",
            "What is the SI unit of force?"
        ],
        "Biology": [
            "Define photosynthesis.",
            "What is a cell?",
            "Name the parts of a plant cell."
        ]
    }
}

# ------------------------------
# PAGE TITLE
# ------------------------------
st.title("📘 Exam Paper Generator")
st.write("Automatically generate an exam paper based on subject, topics, and total marks.")

# ------------------------------
# USER INPUT SECTION
# ------------------------------
subject = st.selectbox("Select Subject", list(QUESTION_BANK.keys()))

topics = st.multiselect(
    "Choose Topics",
    list(QUESTION_BANK[subject].keys()),
    default=list(QUESTION_BANK[subject].keys())[:1]
)

total_marks = st.number_input("Enter Total Marks", min_value=10, max_value=200, step=5)

marks_per_question = st.number_input("Marks per Question", min_value=1, max_value=20, step=1, value=5)

generate_btn = st.button("Generate Exam Paper")

# ------------------------------
# GENERATE EXAM FUNCTION
# ------------------------------
def generate_exam(subject, topics, total_marks, marks_per_question):
    all_questions = []
    for topic in topics:
        all_questions.extend(QUESTION_BANK[subject][topic])

    num_questions = total_marks // marks_per_question

    if num_questions > len(all_questions):
        num_questions = len(all_questions)

    selected_questions = random.sample(all_questions, num_questions)

    exam_df = pd.DataFrame({
        "Q.No": range(1, len(selected_questions) + 1),
        "Question": selected_questions,
        "Marks": [marks_per_question] * len(selected_questions)
    })

    return exam_df

# ------------------------------
# DISPLAY OUTPUT
# ------------------------------
if generate_btn:
    exam_paper = generate_exam(subject, topics, total_marks, marks_per_question)

    st.success("✅ Exam Paper Generated Successfully!")

    st.subheader("📄 Exam Paper")
    st.table(exam_paper)

    # Download as text
    exam_text = ""
    for index, row in exam_paper.iterrows():
        exam_text += f"Q{row['Q.No']}. {row['Question']}  ({row['Marks']} marks)\n"

    st.download_button(
        "Download Exam Paper (.txt)",
        exam_text,
        file_name="exam_paper.txt"
    )
