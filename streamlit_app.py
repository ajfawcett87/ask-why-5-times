import streamlit as st
import os

# --- APPLICATION SETUP ---
st.set_page_config(page_title="Farm Adviser Training Simulator", page_icon="🚜", layout="centered")

# --- CUSTOM BRANDING & LOGO SIDEBAR ---
with st.sidebar:
    # Check if the logo file exists in the GitHub folder
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # Fallback text placeholder if the logo isn't uploaded yet
        st.info("💡 Tip: Upload 'logo.png' to your GitHub repository to see your logo here!")
    
    st.markdown("### 🎓 Course Portal")
    st.write("**Course:** Effective Farmer Communication")
    st.write("**Organization:** Your Organization Name")
    st.markdown("---")
    st.markdown(
        "### 📜 Core Rules Reminder:\n"
        "1. **Validate First:** Acknowledge their stress/hesitation.\n"
        "2. **Open Starters:** Use *What*, *How*, or *Tell me about...*\n"
        "3. **No Closed Questions:** Ban *Do you*, *Have you*, *Is it*."
    )

# --- MAIN PAGE HEADER ---
st.title("🚜 Farm Adviser Chatbot Simulator")
st.subheader("Mastering the '5 Whys' Through Open Questions")
st.write(
    "**Objective:** Guide your farmer client from their surface-level objection down to their core "
    "root cause. You must use **empathy/validation** and **open questions**. Avoid closed questions."
)
st.markdown("---")

# --- ALL 3 SCENARIOS DEFINED ---
SCENARIOS = {
    "Scenario 1: The Tech Skeptic (Sarah)": {
        "farmer_name": "Sarah",
        "topic": "Implementing automated heat-detection collars for a dairy herd",
        "layers": {
            1: {
                "text": "I don't need gadgets. I can spot a cow in heat just fine by looking at them the way my family always has.",
                "hint": "Acknowledge her skill as a stockwoman, then ask an open question about what makes her wary of modern gadgets."
            },
            2: {
                "text": "These tech companies promise the world, but when the internet drops out or a collar breaks, you're stuck waiting days for a technician while your breeding window closes.",
                "hint": "Validate her fear of system failures, then ask an open question to find out if she's had an issue like this happen before."
            },
            3: {
                "text": "We spent fifteen grand on an automatic drafting gate four years ago. It glitched constantly, injured a heifer, and the company refused to refund us. I ended up ripping it out.",
                "hint": "Acknowledge that terrible past experience and the loss of money, then ask an open question about how that affects her view of this new system."
            },
            4: {
                "text": "Stockmanship is what I’ve good at. It’s what my dad taught me. If I let a computer make the breeding decisions, I feel like I’m just a button-pusher on my own land.",
                "hint": "Validate how important her identity and heritage as a hands-on stockwoman are, then ask an open question about her deeper concerns regarding the future of her role."
            },
            5: {
                "text": "Honestly, I'm getting older and I feel overwhelmed by modern farming. I'm terrified that if I can't master this tech, I'll be forced to retire sooner than I want to because I can't keep up.",
                "hint": "Success! You uncovered her fear of obsolescence and losing connection."
            }
        }
    },
    "Scenario 2: The Environmental Resister (John)": {
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
    },
    "Scenario 3: The Burnout Case (Tom)": {
        "farmer_name": "Tom",
        "topic": "Reducing fertilizer inputs and stocking density for a new subsidy scheme",
        "layers": {
            1: {
                "text": "Less stock means less output. You don't make money by producing less food, no matter what the government says.",
                "hint": "Acknowledge the logic of keeping production high, then ask an open question about his experience with relying on government payments."
            },
            2: {
                "text": "The government payments are completely unreliable and change every year. You can't budget a real business on political promises.",
                "hint": "Validate how frustrating policy instability is, then ask an open question about how his current budget pressure is keeping things tight."
            },
            3: {
                "text": "We took out a massive bank loan for a new tractor and machinery shed two years ago. The bank looks at our gross turnover. If our overall output drops, the bank gets nervous, and I can't have them breathing down my neck.",
                "hint": "Acknowledge how heavy bank debt feels, then ask an open question about how managing this loan is impacting his day-to-day life."
            },
            4: {
                "text": "I am working eighty hours a week just to stand still and pay that interest. I don't sleep, I don't see my kids, and I simply do not have the mental energy to learn a whole new farming system right now.",
                "hint": "Show deep empathy for his physical and mental exhaustion, then ask an open question about what support or relief would help him right now."
            },
            5: {
                "text": "I'm just completely spent. I am so tired I can barely think straight, and I'm paralyzed by the fear that one wrong move will bankrupt us. I'm defensive because I'm just trying to survive.",
                "hint": "Success! You uncovered severe mental burnout and acute financial panic."
            }
        }
    }
}

# --- SCENARIO SELECTOR DROP-DOWN ---
selected_key = st.selectbox("🎯 Choose a farming client scenario to practice:", list(SCENARIOS.keys()))
active_scenario = SCENARIOS[selected_key]
farmer_name = active_scenario["farmer_name"]

# Reset state if the user switches scenarios mid-game
if "current_scenario_name" not in st.session_state or st.session_state.current_scenario_name != selected_key:
    st.session_state.current_scenario_name = selected_key
    st.session_state.layer = 1
    st.session_state.strikes = 0
    st.session_state.chat_history = [
        {"role": "farmer", "text": f"**{farmer_name}:** {active_scenario['layers'][1]['text']}"}
    ]
    st.session_state.coach_feedback = None
    st.session_state.game_over = False

# --- EVALUATION LOGIC ENGINE ---
def evaluate_input(user_text):
    text_lower = user_text.lower().strip()
    
    closed_starters = ["do ", "does ", "is ", "are ", "have ", "has ", "can ", "could ", "should ", "would ", "will ", "did ", "am "]
    is_closed = any(text_lower.startswith(starter) for starter in closed_starters) or (text_lower.endswith("?") and any(text_lower.startswith(s) for s in closed_starters))
    
    open_starters = ["what", "how", "tell me", "why", "describe", "share", "explain"]
    is_open = any(starter in text_lower for starter in open_starters)
    
    if is_closed:
        return False, "You used a **closed question** starter (like 'Do you', 'Have you', 'Is it'). Closed questions make farmers defensive. Try using 'What' or 'How' instead."
    
    if not is_open:
        return False, "Your response didn't seem to include a clear, **open-ended question** (using What, How, or 'Tell me about...')."
    
    empathy_keywords = ["understand", "makes sense", "fair enough", "appreciate", "tough", "worry", "risk", "agree", "sounds like", "sorry to hear"]
    has_empathy = any(word in text_lower for word in empathy_keywords) or len(user_text) > 25
    
    if not has_empathy:
        return False, "You jumped straight into a question without explicitly **validating or acknowledging** their feelings first. Farmers need to feel heard before they open up."
        
    return True, "Excellent open question and validation!"

# --- UI DISPLAY LOOP ---
st.write(f"**Current Discussion Topic:** {active_scenario['topic']}")

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
    st.success(f"🎉 **Simulation Complete!** You successfully guided {farmer_name} down to the root cause using open dialogue.")
    if st.button("Reset Current Simulation"):
        st.session_state.layer = 1
        st.session_state.strikes = 0
        st.session_state.chat_history = [{"role": "farmer", "text": f"**{farmer_name}:** {active_scenario['layers'][1]['text']}"}]
        st.session_state.game_over = False
        st.rerun()

elif user_input := st.chat_input(f"Type your response to {farmer_name} here..."):
    st.session_state.chat_history.append({"role": "adviser", "text": f"**You:** {user_input}"})
    
    passed, feedback_msg = evaluate_input(user_input)
    
    if passed:
        st.session_state.strikes = 0
        st.session_state.layer += 1
        current_layer = st.session_state.layer
        
        if current_layer == 5:
            farmer_reply = f"**{farmer_name}:** {active_scenario['layers'][5]['text']} If you can help me navigate this part of the problem, I suppose I'm open to seeing what options we actually have..."
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            st.session_state.game_over = True
        else:
            farmer_reply = f"**{farmer_name}:** {active_scenario['layers'][current_layer]['text']}"
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            
    else:
        st.session_state.strikes += 1
        if st.session_state.strikes >= 2:
            st.session_state.coach_feedback = f"{feedback_msg} \n\n*Coach Tip for Current Layer:* {active_scenario['layers'][st.session_state.layer]['hint']}"
            st.session_state.strikes = 0 
        else:
            farmer_reply = f"**{farmer_name}:** Look, like I said... {active_scenario['layers'][st.session_state.layer]['text']}"
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            
    st.rerun()
