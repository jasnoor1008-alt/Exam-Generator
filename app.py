import streamlit as st
import random
import pandas as pd
from textwrap import dedent

st.set_page_config(page_title="Class 10 Exam Generator — Fixed Blueprint", layout="wide")

# ----------------------------
# FIXED BLUEPRINT (do not change)
# ----------------------------
BLUEPRINT = {
    "Section A": {"count": 20, "marks_each": 1, "desc": "Very short objective / one-mark questions"},
    "Section B": {"count": 5,  "marks_each": 2, "desc": "Short answer — 2 marks"},
    "Section C": {"count": 6,  "marks_each": 3, "desc": "Longer short answers — 3 marks"},
    "Section D": {"count": 4,  "marks_each": 5, "desc": "Long answer / problem solving — 5 marks"},
    "Section E": {"count": 3,  "marks_each": 4, "desc": "Case-based questions (each case has sub-questions totaling 4 marks)"}
}

# ----------------------------
# TOPICS (Class 10 Math)
# ----------------------------
TOPICS = [
    "Real Numbers",
    "Polynomials",
    "Pair of Linear Equations",
    "Quadratic Equations",
    "Arithmetic Progression",
    "Introduction to Trigonometry",
    "Heights and Distances",
    "Circles",
    "Areas related to Circles",
    "Surface Areas & Volumes",
    "Statistics",
    "Probability"
]

# ----------------------------
# QUESTION BANK (per-topic with marks)
# - Each topic has multiple Qs with mark values 1,2,3,5
# - Ensure enough variety so generator can usually satisfy blueprint
# ----------------------------
QUESTION_BANK = {
    "Real Numbers": [
        {"q": "Define irrational numbers.", "m": 1},
        {"q": "State Euclid's Lemma.", "m": 1},
        {"q": "Find the HCF of 84 and 126 by prime factorization.", "m": 2},
        {"q": "Show that sqrt(2) is irrational.", "m": 3},
        {"q": "Prove that every composite number has a prime factor ≤ its square root.", "m": 5},
    ],
    "Polynomials": [
        {"q": "Define a polynomial of degree n.", "m": 1},
        {"q": "What is a zero of a polynomial?", "m": 1},
        {"q": "Divide x^3 - 2x^2 + 3x - 4 by x - 1. Find remainder.", "m": 2},
        {"q": "State and apply the Remainder Theorem for x^3 + 2x^2 - x + 1.", "m": 3},
        {"q": "If α and β are zeros of ax^2+bx+c, express α+β and αβ in terms of a,b,c and prove it.", "m": 5},
    ],
    "Pair of Linear Equations": [
        {"q": "What is a pair of linear equations in two variables?", "m": 1},
        {"q": "Solve: x + y = 5 and x - y = 1.", "m": 2},
        {"q": "Solve using substitution: 2x + 3y = 13 and x - y = 1.", "m": 3},
        {"q": "Discuss graphical method of solving two linear equations.", "m": 1},
        {"q": "A farmer buys chickens and goats. Solve a real world problem using linear equations. (Word problem)", "m": 5},
    ],
    "Quadratic Equations": [
        {"q": "Define quadratic equation.", "m": 1},
        {"q": "Find the discriminant of x^2 - 5x + 6.", "m": 1},
        {"q": "Solve x^2 - 3x - 10 = 0 by factorization.", "m": 2},
        {"q": "Solve x^2 + 4x + 1 = 0 using quadratic formula.", "m": 3},
        {"q": "Form a quadratic equation with given roots 2 and -3 and solve a word problem using it.", "m": 5},
    ],
    "Arithmetic Progression": [
        {"q": "Define AP (arithmetic progression).", "m": 1},
        {"q": "Find the common difference of 5, 8, 11, ...", "m": 1},
        {"q": "Find the 10th term of an AP with a1=3 and d=4.", "m": 2},
        {"q": "Derive formula for sum of first n terms of AP.", "m": 3},
        {"q": "An application problem involving AP (e.g., total savings over months).", "m": 5},
    ],
    "Introduction to Trigonometry": [
        {"q": "What is sin of 30°?", "m": 1},
        {"q": "Define tan θ in a right triangle.", "m": 1},
        {"q": "Prove sin^2θ + cos^2θ = 1.", "m": 3},
        {"q": "Find sin, cos, tan for 45° using a unit triangle.", "m": 2},
        {"q": "Solve a trig problem combining identities (application) .", "m": 5},
    ],
    "Heights and Distances": [
        {"q": "Define angle of elevation.", "m": 1},
        {"q": "What is angle of depression?", "m": 1},
        {"q": "A simple heights-and-distances problem: find height using tan given distance.", "m": 2},
        {"q": "Solve a multi-step heights and distances question (involving two angles).", "m": 3},
        {"q": "Complex application: tower and two observers (word problem).", "m": 5},
    ],
    "Circles": [
        {"q": "Define a tangent to a circle.", "m": 1},
        {"q": "State the relation between angle subtended by diameter.", "m": 1},
        {"q": "Find equation of circle with given centre and radius (conceptual).", "m": 2},
        {"q": "Prove that the angle in a semicircle is a right angle.", "m": 3},
        {"q": "A geometry problem requiring proofs about chords and arcs.", "m": 5},
    ],
    "Areas related to Circles": [
        {"q": "Formula for area of a circle.", "m": 1},
        {"q": "Find area of sector with radius 7 and angle 60°.", "m": 2},
        {"q": "Find shaded area between two concentric circles (ring)", "m": 3},
        {"q": "Composite area problem involving circles and triangles.", "m": 5},
    ],
    "Surface Areas & Volumes": [
        {"q": "Define volume of a cube.", "m": 1},
        {"q": "Formula for surface area of a sphere.", "m": 1},
        {"q": "Find volume of a cone with radius r and height h.", "m": 3},
        {"q": "Problem: find curved surface area of a cylinder.", "m": 2},
        {"q": "A complex solids problem mixing two solids (e.g., cylinder with hemispherical ends).", "m": 5},
    ],
    "Statistics": [
        {"q": "Define mean of a data set.", "m": 1},
        {"q": "Find median of 2, 3, 7, 9, 10.", "m": 1},
        {"q": "Compute mean for a small frequency distribution.", "m": 3},
        {"q": "Draw and interpret a bar graph or frequency polygon (describe steps).", "m": 2},
        {"q": "A statistics application requiring interpretation and calculation from grouped data.", "m": 5},
    ],
    "Probability": [
        {"q": "Define probability of an event.", "m": 1},
        {"q": "Find probability of getting an even number on rolling a die.", "m": 1},
        {"q": "Two-step probability problem without replacement.", "m": 3},
        {"q": "Find probability of drawing two red balls from a bag (word problem).", "m": 2},
        {"q": "A complex probability question (combined events).", "m": 5},
    ],
}

# ----------------------------
# CASE STUDY BANK (Section E)
# Each case is a passage + list of (subq_text, marks)
# Total marks for each case must be 4 (per blueprint)
# ----------------------------
CASE_BANK = [
    {
        "case": dedent("""
            A small water tank has the shape of a cylinder with radius 3 m and height 4 m.
            Water is being filled at a steady rate. The tank leaks at the rate of 2 liters/min.
            """).strip(),
        "subqs": [
            ("Convert the tank dimensions to cm and find the volume in cubic centimeters. (2 marks)", 2),
            ("If the filling rate is 5000 cm³/min, calculate net rate of rise considering leak. (2 marks)", 2),
        ]
    },
    {
        "case": dedent("""
            A school arranged a survey of scores of students in a 50 mark test.
            The frequency distribution is: 0-10:5, 11-20:10, 21-30:8, 31-40:4, 41-50:3.
            """).strip(),
        "subqs": [
            ("Compute the mean using mid-point method (2 marks).", 2),
            ("State which class interval has the highest frequency and comment (2 marks).", 2),
        ]
    },
    {
        "case": dedent("""
            A ladder leans against a wall making an angle of 60° with the ground.
            The foot of the ladder is 4 m away from the wall.
            """).strip(),
        "subqs": [
            ("Find the length of the ladder. (2 marks)", 2),
            ("If the ladder is pulled down so the foot is 6 m away, what is the new angle? Use trig approx. (2 marks)", 2),
        ]
    },
    {
        "case": dedent("""
            A cone and a cylinder have the same base radius r. The height of cone is h and cylinder is 2h.
            """).strip(),
        "subqs": [
            ("Write volumes of cone and cylinder in terms of r and h. (2 marks)", 2),
            ("Find ratio of volumes cone:cylinder. (2 marks)", 2),
        ]
    },
]

# ----------------------------
# Helper: flatten questions from selected topics and separate by marks
# ----------------------------
def gather_by_mark(selected_topics):
    buckets = {1: [], 2: [], 3: [], 5: []}
    for t in selected_topics:
        qs = QUESTION_BANK.get(t, [])
        for q in qs:
            m = q["m"]
            if m in buckets:
                buckets[m].append({"q": q["q"], "m": m, "topic": t})
    return buckets

# ----------------------------
# GENERATOR: pick exact counts per blueprint
# ----------------------------
def generate_paper(selected_topics):
    # gather
    buckets = gather_by_mark(selected_topics)

    # desired counts for sections mapping marks -> desired_count
    desired = {
        1: BLUEPRINT["Section A"]["count"],
        2: BLUEPRINT["Section B"]["count"],
        3: BLUEPRINT["Section C"]["count"],
        5: BLUEPRINT["Section D"]["count"]
    }
    chosen = {"A": [], "B": [], "C": [], "D": [], "E": []}
    # Check availability and pick
    for m, need in desired.items():
        pool = buckets.get(m, [])
        if len(pool) < need:
            return None, f"Not enough {m}-mark questions available across selected topics. Needed {need}, found {len(pool)}."
        chosen_pool = random.sample(pool, need)
        if m == 1:
            chosen["A"] = chosen_pool
        elif m == 2:
            chosen["B"] = chosen_pool
        elif m == 3:
            chosen["C"] = chosen_pool
        elif m == 5:
            chosen["D"] = chosen_pool

    # Section E: choose cases (each case is 4 marks)
    if len(CASE_BANK) < BLUEPRINT["Section E"]["count"]:
        return None, "Not enough case studies in CASE_BANK."
    chosen_cases = random.sample(CASE_BANK, BLUEPRINT["Section E"]["count"])
    chosen["E"] = chosen_cases

    return chosen, "OK"

# ----------------------------
# UI: Sidebar for topic selection (default: all)
# ----------------------------
st.sidebar.header("Select Topics (default: all)")
topic_checks = {}
cols = st.sidebar.columns(2)
for i, topic in enumerate(TOPICS):
    with cols[i % 2]:
        topic_checks[topic] = st.checkbox(topic, value=True)

selected_topics = [t for t, v in topic_checks.items() if v]
if not selected_topics:
    st.sidebar.error("Please select at least one topic.")

# Info about blueprint
st.header("📗 Class 10 — Exam Generator (Fixed Blueprint)")
st.markdown("""
This generator **always** produces the same section structure:

- **Section A:** 20 × 1-mark  
- **Section B:** 5 × 2-marks  
- **Section C:** 6 × 3-marks  
- **Section D:** 4 × 5-marks  
- **Section E:** 3 × case studies (each worth 4 marks; sub-questions total 4)
""")

st.write("Selected topics:", ", ".join(selected_topics))
st.write("Total marks produced by blueprint: **80**")

# Generate button
if st.button("Generate Exam Paper"):
    if not selected_topics:
        st.error("Select topics from the sidebar before generating.")
    else:
        paper, status = generate_paper(selected_topics)
        if paper is None:
            st.error(status)
        else:
            st.success("✅ Exam paper generated")
            # Display section-wise
            def section_table(items, include_topic=False):
                rows = []
                for i, it in enumerate(items, start=1):
                    if include_topic:
                        rows.append({"Q.No": i, "Question": it["q"], "Marks": it["m"], "Topic": it["topic"]})
                    else:
                        rows.append({"Q.No": i, "Question": it["q"], "Marks": it["m"]})
                return pd.DataFrame(rows)

            # Section A
            st.subheader("Section A — 20 × 1 mark (Very short questions)")
            dfA = section_table(paper["A"], include_topic=True)
            st.table(dfA)

            # Section B
            st.subheader("Section B — 5 × 2 marks")
            dfB = section_table(paper["B"], include_topic=True)
            st.table(dfB)

            # Section C
            st.subheader("Section C — 6 × 3 marks")
            dfC = section_table(paper["C"], include_topic=True)
            st.table(dfC)

            # Section D
            st.subheader("Section D — 4 × 5 marks")
            dfD = section_table(paper["D"], include_topic=True)
            st.table(dfD)

            # Section E (case studies)
            st.subheader("Section E — 3 Case Studies (Each case = 4 marks)")
            for idx, case in enumerate(paper["E"], start=1):
                st.markdown(f"**Case {idx}:** {case['case']}")
                subrows = []
                for sidx, (text, marks) in enumerate(case["subqs"], start=1):
                    subrows.append({"Q": f"{idx}.{sidx}", "Sub-question": text, "Marks": marks})
                st.table(pd.DataFrame(subrows))

            # Build downloadable text output (structured)
            out_lines = []
            out_lines.append("CLASS 10 — MATHEMATICS\n")
            out_lines.append("Total Marks: 80\n\n")

            # A
            out_lines.append("SECTION A — 20 × 1 mark\n")
            for i, it in enumerate(paper["A"], start=1):
                out_lines.append(f"A{i}. {it['q']} ({it['m']}m) [{it['topic']}]\n")
            out_lines.append("\n")

            # B
            out_lines.append("SECTION B — 5 × 2 marks\n")
            for i, it in enumerate(paper["B"], start=1):
                out_lines.append(f"B{i}. {it['q']} ({it['m']}m) [{it['topic']}]\n")
            out_lines.append("\n")

            # C
            out_lines.append("SECTION C — 6 × 3 marks\n")
            for i, it in enumerate(paper["C"], start=1):
                out_lines.append(f"C{i}. {it['q']} ({it['m']}m) [{it['topic']}]\n")
            out_lines.append("\n")

            # D
            out_lines.append("SECTION D — 4 × 5 marks\n")
            for i, it in enumerate(paper["D"], start=1):
                out_lines.append(f"D{i}. {it['q']} ({it['m']}m) [{it['topic']}]\n")
            out_lines.append("\n")

            # E (cases)
            out_lines.append("SECTION E — Case Studies (Each case = 4 marks)\n")
            for idx, case in enumerate(paper["E"], start=1):
                out_lines.append(f"Case {idx}:\n{case['case']}\n")
                for sidx, (text, marks) in enumerate(case["subqs"], start=1):
                    out_lines.append(f"  {idx}.{sidx} {text} ({marks}m)\n")
                out_lines.append("\n")

            text_output = "".join(out_lines)

            st.download_button("Download Exam (.txt)", text_output, file_name="class10_exam_paper.txt")

# Footer / tips
st.markdown("---")
st.caption("Notes: If generator reports 'not enough questions', enable more topics in the sidebar or expand the QUESTION_BANK in the code with additional questions for the shortfall topics.")
