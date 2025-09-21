import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd
import re

# --- Configuration ---
FLASK_API_URL = "https://omr-evaluation-app.onrender.com/predict"

# --- Page Setup ---
st.set_page_config(
    page_title="OMR Grading Application",
    layout="wide"
)

# --- Helper Function (No changes needed) ---
def parse_answer_key(uploaded_file):
    """
    Parses the uploaded answer key (CSV or Excel) into a dictionary
    and also returns the section names from the header.
    """
    answer_key = {}
    section_names = []
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        section_names = df.columns.tolist()

        for col in df.columns:
            for item in df[col].dropna():
                item_str = str(item)
                match = re.match(r'^\s*(\d+)\s*[-.\s]\s*([a-zA-Z])', item_str)
                if match:
                    q_num = int(match.group(1))
                    ans = match.group(2).strip().lower()
                    answer_key[q_num] = ans
        
        if not answer_key:
            st.error("Could not parse the answer key. Please ensure it follows the format 'QuestionNumber - Answer'.")
            return None, None
            
        return answer_key, section_names

    except Exception as e:
        st.error(f"Error reading or parsing the answer key file: {e}")
        return None, None

# --- Main Application UI ---
st.title("OMR Grading Application")
st.markdown("This tool automates the grading of OMR sheets by comparing them against a provided answer key.")
st.markdown("---")

# --- File Upload Section ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Step 1: Upload OMR Sheet")
    uploaded_image = st.file_uploader(
        "Upload the scanned image of the filled OMR sheet.",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
with col2:
    st.subheader("Step 2: Upload Answer Key")
    uploaded_key = st.file_uploader(
        "Upload the Excel or CSV file with correct answers.",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

# --- Grading and Results ---
if uploaded_image and uploaded_key:
    if st.button("Process and Grade Sheet", type="primary", use_container_width=True):
        answer_key, section_names = parse_answer_key(uploaded_key)
        
        if answer_key and section_names:
            with st.spinner("Processing... Please wait."):
                try:
                    img_bytes = uploaded_image.getvalue()
                    files = {'file': (uploaded_image.name, img_bytes, uploaded_image.type)}
                    response = requests.post(FLASK_API_URL, files=files)

                    if response.status_code == 200:
                        results = response.json()
                        detected_answers = results.get('predictions', [])
                        
                        # --- Grading Logic ---
                        correct_count = 0
                        total_questions = len(detected_answers)
                        ranges = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
                        section_ranges = {name: ranges[i] for i, name in enumerate(section_names) if i < len(ranges)}
                        section_scores = {name: {'correct': 0, 'total': 0} for name in section_names}

                        for pred in detected_answers:
                            q_num, detected_ans = pred['question'], pred['answer']
                            correct_ans = answer_key.get(q_num)
                            is_correct = correct_ans and detected_ans.lower() == correct_ans
                            if is_correct: correct_count += 1
                            
                            for name, (start, end) in section_ranges.items():
                                if start <= q_num <= end:
                                    section_scores[name]['total'] += 1
                                    if is_correct: section_scores[name]['correct'] += 1
                                    break
                        
                        # --- Results Display ---
                        st.markdown("---")
                        st.header("Grading Results")
                        summary_tab, details_tab = st.tabs(["Score Summary", "Detailed Report"])

                        with summary_tab:
                            if total_questions > 0:
                                st.metric(
                                    label="Total Score", 
                                    value=f"{correct_count} / {total_questions}",
                                    delta=f"{round((correct_count / total_questions) * 100, 1)}%"
                                )
                                st.markdown("##### Section-wise Performance")
                                score_cols = st.columns(len(section_names))
                                for i, name in enumerate(section_names):
                                    with score_cols[i]:
                                        score = section_scores[name]
                                        st.metric(label=name, value=f"{score['correct']} / {score['total']}")
                            else:
                                st.warning("No answers were detected on the OMR sheet.")

                        with details_tab:
                            st.write("Review of each question:")
                            res_cols = st.columns(5)
                            for i, pred in enumerate(detected_answers):
                                q_num, detected_ans = pred['question'], pred['answer']
                                correct_ans = answer_key.get(q_num)
                                with res_cols[i % 5]:
                                    if correct_ans and detected_ans.lower() == correct_ans:
                                        st.success(f"Q{q_num}: {detected_ans.upper()}")
                                    else:
                                        correct_ans_display = correct_ans.upper() if correct_ans else "N/A"
                                        st.error(f"Q{q_num}: {detected_ans.upper()} (Key: {correct_ans_display})")
                    
                    else:
                        st.error(f"Error from server: {response.json().get('error', 'Unknown error')}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the backend server. Please ensure it is running. Error: {e}")
        else:
            st.error("The answer key is empty or incorrectly formatted. Please check the file and try again.")
else:
    st.info("Please upload both an OMR sheet and an answer key to proceed with grading.")

# --- About Section ---
st.markdown("---")
st.subheader("About the Developers")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Naveen Jayaraj**")
    st.markdown("B.Tech CSE with AIML, 3rd Year")
    st.link_button("LinkedIn Profile", "https://www.linkedin.com/")
with col2:
    st.markdown("**Shreya Ravi K**")
    st.markdown("B.Tech CSE, 3rd Year")
    st.link_button("LinkedIn Profile", "https://www.linkedin.com/")