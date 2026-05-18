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
def evaluate_input(user_text):
    text_lower = user_text.lower().strip()
    
    # 1. Check for Closed Question Openers (Fail Condition)
    closed_starters = ["do ", "does ", "is ", "are ", "have ", "has ", "can ", "could ", "should ", "would ", "will ", "did ", "am "]
    is_closed = any(text_lower.startswith(starter) for starter in closed_starters) or (text_lower.endswith("?") and any(text_lower.startswith(s) for s in closed_starters))
    
    # 2. Check for Open Question Openers (Pass Condition helper)
    open_starters = ["what", "how", "tell me", "why", "describe", "share"]
    is_open = any(starter in text_lower for starter in open_starters)
    
    # Strict Assessment Rules
    if is_closed:
        return False, "You used a **closed question** starter (like 'Do you', 'Have you', 'Is it'). Closed questions make farmers defensive. Try using 'What' or 'How' instead."
    
    if not is_open:
        return False, "Your response didn't seem to include a clear, **open-ended question** (using What, How, or 'Tell me about...')."
    
    # Simple validation heuristic
    empathy_keywords = ["understand", "makes sense", "fair enough", "appreciate", "tough", "worry", "risk", "agree"]
    has_empathy = any(word in text_lower for word in empathy_keywords) or len(user_text) > 25
    
    if not has_empathy:
        return False, "You jumped straight into a question without explicitly **validating or acknowledging** John's feelings first. Farmers need to feel heard before they open up."
        
    return True, "Excellent open question and validation!"

# --- UI DISPLAY LOOP ---
for message in st.session_state.chat_history:
    if message["role"] == "farmer":
        st.chat_message("user", avatar="👨‍🌾").write(message["text"])
    elif message["role"] == "adviser":
        st.chat_message("assistant", avatar="💼").write(message["text"])

if st.session_state.coach_feedback:
    st.error(f"🏽 **[AI COACH]:** {st.session_state.coach_feedback}")
    st.session_state.coach_feedback = None 

if st.session_state.game_over:
    st.balloons()
    st.success("🎉 **Simulation Complete!** You successfully peeled back all 5 layers using open dialogue.")
    if st.button("Reset Simulation"):
        st.session_state.layer = 1
        st.session_state.strikes = 0
        st.session_state.chat_history = [{"role": "farmer", "text": f"**John:** {SCENARIO['layers'][1]['text']}"}]
        st.session_state.game_over = False
        st.rerun()

elif user_input := st.chat_input("Type your response to John here..."):
    st.session_state.chat_history.append({"role": "adviser", "text": f"**You:** {user_input}"})
    
    passed, feedback_msg = evaluate_input(user_input)
    
    if passed:
        st.session_state.strikes = 0
        st.session_state.layer += 1
        current_layer = st.session_state.layer
        
        if current_layer == 5:
            farmer_reply = f"**John:** {SCENARIO['layers'][5]['text']} If you can help me phrase this to him so he doesn't think I'm ruining the farm, I guess I'm willing to look at the budget numbers with you..."
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            st.session_state.game_over = True
        else:
            farmer_reply = f"**John:** {SCENARIO['layers'][current_layer]['text']}"
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            
    else:
        st.session_state.strikes += 1
        if st.session_state.strikes >= 2:
            st.session_state.coach_feedback = f"{feedback_msg} \n\n*Coach Tip for Current Layer:* {SCENARIO['layers'][st.session_state.layer]['hint']}"
            st.session_state.strikes = 0 
        else:
            farmer_reply = f"**John:** Look, like I said... {SCENARIO['layers'][st.session_state.layer]['text']}"
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            
    st.rerun()
