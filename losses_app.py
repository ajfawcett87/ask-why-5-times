import streamlit as st
import os

# --- APPLICATION SETUP ---
st.set_page_config(page_title="Farmer Loss-Spotting Simulator", page_icon="🧠", layout="centered")

# --- BRANDING SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("### 🎓 Module 4 Portal")
    st.write("**Course:** The Farm-Gate Influence Lab")
    st.write("**Topic:** Decoding the 4 Common Losses")
    st.markdown("---")
    st.markdown(
        "### 🔍 The 4 Common Losses:\n"
        "- **Control:** Losing autonomy or decision-making power.\n"
        "- **Certainty:** Loss of predictability or shifting goalposts.\n"
        "- **Competence:** Lifelong skills/expertise feeling obsolete.\n"
        "- **Identity/Legacy:** Threat to family heritage or pride."
    )

st.title("🧠 The '4 Common Losses' Diagnostic Chatbot")
st.write(
    "**Objective:** Chat with the farmer client. Listen closely to their frustrations. "
    "When you spot one of the 4 common losses, type **'DIAGNOSIS: [Loss Name]'** followed by your reason "
    "to see if your diagnostic hearing is correct!"
)
st.markdown("---")

# --- LOSS SCENARIOS DATA ---
LOSS_SCENARIOS = [
    {
        "farmer": "Arthur",
        "intro": "Arthur is a 68-year-old traditional beef farmer facing new regional environmental regulations.",
        "first_line": "They expect me to log into some government portal every time I move cattle between fields to track soil carbon impact. I don't even own a smartphone! I've managed these pastures by eye for forty years. Now some bureaucrat thinks a piece of software knows my grass better than I do.",
        "correct_loss": "competence",
        "coach_explanation": "Arthur is experiencing a threat to his **Competence**. He prides himself on his lifelong, instinctive skill ('managed these pastures by eye for forty years') and feels degraded by tech requirements that make his hard-won expertise feel completely irrelevant."
    },
    {
        "farmer": "Gary",
        "intro": "Gary is a third-generation tenant farmer discussing a new corporate contract option.",
        "first_line": "The supermarket wants us to sign an exclusive supply deal, but their contract template says they can audit my barns with 2 hours' notice and reject a shipment based on 'market fluctuations.' It feels like I'm becoming an underpaid manager for them instead of running my own family business.",
        "correct_loss": "control",
        "coach_explanation": "Gary is reacting to a loss of **Control**. His core frustration stems from losing his autonomy and decision-making independence ('underpaid manager for them instead of running my own family business')."
    }
]

# --- STATE MANAGEMENT ---
if "current_case" not in st.session_state:
    st.session_state.current_case = 0
if "chat_history" not in st.session_state:
