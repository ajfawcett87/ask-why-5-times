import streamlit as st

# --- APPLICATION SETUP ---
st.set_page_config(page_title="Farm Adviser Training Simulator", page_icon="🚜", layout="centered")

st.title("🚜 Farm Adviser Chatbot Simulator")
st.subheader("Mastering the '5 Whys' Through Open Questions")
st.write(
    "**Objective:** Guide the farmer, John, from his surface-level objection down to his core "
    "root cause. You must use **empathy/validation** and **open questions** (What, How, Tell me about...). "
    "Avoid closed questions (Do, Is, Have, Can)."
)
st.markdown("---")

# --- SCENARIO DATA DEFINITION ---
SCENARIO = {
    "farmer_name": "John",
    "topic": "Switching to multi-species herbal leys / cover crops",
    "layers": {
        1: {
            "text": "Look, I appreciate you coming out, but this herbal ley stuff is just a fad for hobby farmers. Traditional ryegrass and clover works perfectly fine on my dirt.",
            "hint": "Acknowledge his success with ryegrass, then ask an open question about his initial hesitation."
        },
        2: {
            "text": "It's just too risky. The establishment is expensive, and those seed mixes cost nearly double. I simply can't afford a crop failure right now.",
            "hint": "Validate his financial caution, then ask an open question to find out why a failure right now is particularly terrifying."
        },
        3: {
            "text": "Well, look at my neighbors. They are intensive arable guys. If they see my fields looking 'weedy' and messy with all these different plants, they're going to think I’ve given up or gone broke.",
            "hint": "Acknowledge the pressure of local reputation, then ask an open question about who specifically he is worried about judging him."
        },
        4: {
            "text": "It's my father. He still owns the land and walks the fields every Sunday. If he sees me planting what he considers 'weeds,' we will have a massive blowout argument about how I'm ruining his life's legacy.",
            "hint": "Validate how tough family dynamics are, then ask an open question to uncover the ultimate root fear beneath this conflict."
        },
        5: {
            "text": "Honestly... I'm just terrified of letting him down. I want to improve the soil, but I can't bear the thought of him looking at me like I failed him and ruined his legacy. I just want his approval.",
            "hint": "Success! You reached the root cause."
        }
    }
}

# --- STATE MANAGEMENT ---
if "layer" not in st.session_state:
    st.session_state.layer = 1
if "strikes" not in st.session_state:
    st.session_state.strikes = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "farmer", "text": f"**John:** {SCENARIO['layers'][1]['text']}"}
    ]
if "coach_feedback" not in st.session_state:
    st.session_state.coach_feedback = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- EVALUATION LOGIC ENGINE ---
def evaluate_input(user
