import streamlit as st
import os
import re
import random

# --- APPLICATION SETUP ---
st.set_page_config(page_title="Farm Adviser Training Simulator", page_icon="🚜", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .rule-violated { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
    .rule-ok { background-color: #d4edda; border-left: 4px solid #28a745; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
    .layer-progress { font-size: 0.85em; color: #666; margin-bottom: 4px; }
    .summary-card { background: #f8f9fa; border-radius: 8px; padding: 16px; margin: 8px 0; }
    .strike-dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 4px; }
    .strike-used { background-color: #dc3545; }
    .strike-available { background-color: #dee2e6; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.info("💡 Upload 'logo.png' to your GitHub repo to see your logo here.")

    st.markdown("### 🎓 Course Portal")
    st.write("**Course:** The Farm-Gate Influence Lab")
    st.write("**Organisation:** EmpowerAg Ltd")
    st.markdown("---")
    st.markdown("### 📜 The Three Rules")
    st.markdown("""
**Rule 1 — Validate First**
Acknowledge their stress or hesitation before anything else.

**Rule 2 — Open Starters**
Begin questions with *What*, *How*, or *Tell me about...*

**Rule 3 — No Closed Questions**
Banned: *Do you*, *Have you*, *Is it*, *Can you*, *Would you*
""")
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    if "total_strikes" in st.session_state:
        st.write(f"Total strikes this session: **{st.session_state.total_strikes}**")
    if "scenarios_completed" in st.session_state:
        st.write(f"Scenarios completed: **{st.session_state.scenarios_completed}**")


# --- SCENARIOS ---
SCENARIOS = {
    "Scenario 1: The Tech Sceptic (Sarah)": {
        "farmer_name": "Sarah",
        "topic": "Implementing automated heat-detection collars for a dairy herd",
        "layers": {
            1: {
                "text": "I don't need gadgets. I can spot a cow in heat just fine by looking at them the way my family always has.",
                "hint": "Acknowledge her skill as a stockwoman, then ask an open question about what makes her wary of modern gadgets.",
                "warm_replies": [
                    "Aye, well... when you put it like that, I suppose it's not so much the collars themselves. It's more that every time something breaks, you're at the mercy of some customer service line that's never set foot on a farm.",
                    "That's fair. I don't hate all technology, I suppose. It's more that I've been let down before and I can't afford it happening again during breeding season."
                ],
                "cold_replies": [
                    "That's not really what I'm saying though, is it? I'm saying I don't need them. I know my cows.",
                    "Right. Like I said. I manage fine as it is."
                ]
            },
            2: {
                "text": "These tech companies promise the world, but when the internet drops out or a collar breaks, you're stuck waiting days for a technician while your breeding window closes.",
                "hint": "Validate her fear of system failures, then ask an open question about whether she's had a specific experience like this.",
                "warm_replies": [
                    "We spent fifteen grand on an automatic drafting gate four years ago. It glitched constantly, injured a heifer, and the company refused a refund. I ripped it out myself in the end.",
                    "Four years ago we had a similar nightmare with automated drafting. Cost us a fortune and the company just washed their hands of it."
                ],
                "cold_replies": [
                    "Yes, exactly what I said. It's a reliability problem.",
                    "That's my point. These systems fail and you're left holding the bag."
                ]
            },
            3: {
                "text": "We spent fifteen grand on an automatic drafting gate four years ago. It glitched constantly, injured a heifer, and the company refused to refund us. I ended up ripping it out.",
                "hint": "Acknowledge that terrible experience and the financial loss, then ask an open question about how it affects her view of this new system.",
                "warm_replies": [
                    "Stockmanship is what I'm good at. It's what my dad taught me. If I let a computer make the breeding decisions, I feel like I'm just a button-pusher on my own farm.",
                    "It's not just about the money. It's more that I feel like farming is turning into something I don't recognise, and I'm not sure where I fit in it anymore."
                ],
                "cold_replies": [
                    "Exactly. So why would I take that risk again?",
                    "So you can see why I'm not rushing into another one of these systems."
                ]
            },
            4: {
                "text": "Stockmanship is what I'm good at. It's what my dad taught me. If I let a computer make the breeding decisions, I feel like I'm just a button-pusher on my own land.",
                "hint": "Validate how important her identity and heritage as a stockwoman are, then ask an open question about her deeper concerns for the future.",
                "warm_replies": [
                    "Honestly, I'm getting older and I feel overwhelmed by modern farming. I'm terrified that if I can't master this tech, I'll be forced to retire sooner than I want because I can't keep up.",
                    "If I'm being straight with you... I worry I'm being left behind. That one day the farm will need someone younger who understands all this, and I won't have a place in it anymore."
                ],
                "cold_replies": [
                    "It's just not something I want to get into.",
                    "I've said my piece. It's about identity. Leave it there."
                ]
            },
            5: {
                "text": "Honestly, I'm getting older and I feel overwhelmed by modern farming. I'm terrified that if I can't master this tech, I'll be forced to retire sooner than I want because I can't keep up.",
                "hint": "You've done it — root cause reached.",
                "warm_replies": [],
                "cold_replies": []
            }
        }
    },
    "Scenario 2: The Environmental Resister (John)": {
        "farmer_name": "John",
        "topic": "Switching to multi-species herbal leys / cover crops",
        "layers": {
            1: {
                "text": "Look, I appreciate you coming out, but this herbal ley stuff is just a fad for hobby farmers. Traditional ryegrass and clover works perfectly fine on my ground.",
                "hint": "Acknowledge his success with ryegrass, then ask an open question about his initial hesitation.",
                "warm_replies": [
                    "It's just too risky. The establishment is expensive, and those seed mixes cost nearly double. I simply can't afford a crop failure right now.",
                    "Cost is the main thing. I'm not made of money and I can't gamble on something unproven when margins are what they are."
                ],
                "cold_replies": [
                    "Aye. So like I said — ryegrass works.",
                    "Glad you see it. So I'm not sure what we're discussing here."
                ]
            },
            2: {
                "text": "It's just too risky. The establishment is expensive, and those seed mixes cost nearly double. I simply can't afford a crop failure right now.",
                "hint": "Validate his financial caution, then ask an open question about why a failure right now is particularly worrying.",
                "warm_replies": [
                    "Well, look at my neighbours. They're intensive arable guys. If they see my fields looking weedy and messy with all these different plants, they'll think I've given up or gone broke.",
                    "It's partly the neighbours. Round here, a tidy field matters. If it looks a mess, people talk."
                ],
                "cold_replies": [
                    "Because I just can't. Simple as that.",
                    "Any failure right now would be bad. That's all I'll say."
                ]
            },
            3: {
                "text": "It's my father. He still owns the land and walks the fields every Sunday. If he sees me planting what he considers weeds, we'll have a massive blowout about how I'm ruining his life's work.",
                "hint": "Validate how tough that family dynamic is, then ask an open question to get underneath this conflict.",
                "warm_replies": [
                    "Honestly... I'm just terrified of letting him down. I want to improve the soil, but I can't bear the thought of him looking at me like I've failed him. I just want his approval.",
                    "I suppose at the bottom of it, I've spent thirty years trying to prove I can run this place as well as he did. I'm not sure I've managed it yet."
                ],
                "cold_replies": [
                    "It just is what it is with him.",
                    "That's family farming for you. Nothing more to say."
                ]
            },
            4: {
                "text": "It's my father. He still owns the land and walks the fields every Sunday. If he sees me planting what he considers weeds, we'll have a massive blowout about how I'm ruining his life's work.",
                "hint": "Validate the family pressure, then ask what's really underneath this for him personally.",
                "warm_replies": [
                    "Honestly... I just want his approval. I've spent thirty years trying to prove I can run this place as well as he did.",
                    "I suppose the truth is I'm scared of disappointing him more than I'm scared of the crop failing."
                ],
                "cold_replies": [
                    "It is what it is.",
                    "Family's complicated. Leave it at that."
                ]
            },
            5: {
                "text": "Honestly... I'm just terrified of letting him down. I want to improve the soil, but I can't bear the thought of him looking at me like I failed him and ruined his legacy. I just want his approval.",
                "hint": "Root cause reached.",
                "warm_replies": [],
                "cold_replies": []
            }
        }
    },
    "Scenario 3: The Burnout Case (Tom)": {
        "farmer_name": "Tom",
        "topic": "Reducing fertiliser inputs and stocking density for a new subsidy scheme",
        "layers": {
            1: {
                "text": "Less stock means less output. You don't make money by producing less food, no matter what the government says.",
                "hint": "Acknowledge the logic of keeping production high, then ask an open question about his experience relying on government payments.",
                "warm_replies": [
                    "The government payments are completely unreliable and change every year. You can't budget a real business on political promises.",
                    "I've been farming twenty years. Every time I've built a plan around a government scheme, they've changed it halfway through. I'm not doing it again."
                ],
                "cold_replies": [
                    "That's what I said. Less output, less money.",
                    "You can trust the government if you want. I don't."
                ]
            },
            2: {
                "text": "The government payments are completely unreliable and change every year. You can't budget a real business on political promises.",
                "hint": "Validate how frustrating policy instability is, then ask an open question about how current budget pressure is affecting things.",
                "warm_replies": [
                    "We took out a massive bank loan for a new tractor and machinery shed two years ago. If our output drops, the bank gets nervous, and I can't have them breathing down my neck.",
                    "It's the bank, mainly. Big loan two years ago. They watch our turnover closely and if it dips, I'll be on the phone with them every week."
                ],
                "cold_replies": [
                    "Budget's tight. That's all you need to know.",
                    "Let's just say there's not a lot of room for experiments right now."
                ]
            },
            3: {
                "text": "We took out a massive bank loan for a new tractor and machinery shed two years ago. The bank looks at our gross turnover. If our overall output drops, the bank gets nervous, and I can't have them breathing down my neck.",
                "hint": "Acknowledge how heavy that debt feels, then ask an open question about how managing it is affecting his day-to-day life.",
                "warm_replies": [
                    "I'm working eighty hours a week just to stand still and pay that interest. I don't sleep properly, I barely see my kids. I don't have the mental energy to learn a whole new farming system.",
                    "Honestly? I'm exhausted. Properly exhausted. I can't think straight half the time and the last thing I need is another thing to manage."
                ],
                "cold_replies": [
                    "It affects everything. That's how it is.",
                    "It's just constant pressure. I manage."
                ]
            },
            4: {
                "text": "I am working eighty hours a week just to stand still and pay that interest. I don't sleep, I don't see my kids, and I simply do not have the mental energy to learn a whole new farming system right now.",
                "hint": "Show deep empathy for his exhaustion, then ask what support would actually make a difference right now.",
                "warm_replies": [
                    "I'm just completely spent. I'm paralysed by the fear that one wrong move will bankrupt us. I'm defensive because I'm just trying to survive.",
                    "Survival mode, that's what this is. Every day. I'm not looking for opportunities — I'm trying not to go under."
                ],
                "cold_replies": [
                    "Support would be nice. Not sure what that looks like.",
                    "I just need less on my plate. Simple as that."
                ]
            },
            5: {
                "text": "I'm just completely spent. I am so tired I can barely think straight, and I'm paralysed by the fear that one wrong move will bankrupt us. I'm defensive because I'm just trying to survive.",
                "hint": "Root cause reached.",
                "warm_replies": [],
                "cold_replies": []
            }
        }
    }
}

MAX_LAYERS = 5
MAX_ATTEMPTS_PER_LAYER = 3


# --- IMPROVED EVALUATION ENGINE ---
def evaluate_response(user_text):
    """
    Returns: (passed: bool, rule_broken: str|None, feedback: str)
    rule_broken is one of: "closed_question", "no_open_question", "no_validation", None
    """
    text = user_text.strip()
    text_lower = text.lower()

    # Too short to be a proper response
    if len(text.split()) < 4:
        return False, "no_validation", (
            "That's too brief to count as a real response. "
            "A single word or short phrase isn't enough — your farmer needs to feel heard."
        )

    # Rule 3: Check for closed question starters
    # Must check the actual question part, not just the opening words
    sentences = re.split(r'[.!?]+', text_lower)
    questions = [s.strip() for s in sentences if '?' in text_lower or any(
        s.strip().startswith(starter) for starter in [
            "do ", "does ", "is ", "are ", "have ", "has ",
            "can ", "could ", "should ", "would ", "will ", "did ", "am "
        ]
    )]

    closed_starters = [
        "do ", "does ", "is ", "are ", "have ", "has ",
        "can ", "could ", "should ", "would ", "will ", "did ", "am "
    ]
    for sentence in sentences:
        sentence = sentence.strip()
        if any(sentence.startswith(s) for s in closed_starters) and len(sentence) > 3:
            return False, "closed_question", (
                "⚠️ **Rule 3 broken — Closed question detected.** "
                f"Your response appears to start a question with a closed word like 'Do', 'Have', 'Is', or 'Can'. "
                "These put farmers on the defensive. Swap it for 'What' or 'How' instead."
            )

    # Rule 2: Must contain an open question
    open_patterns = [
        r'\bwhat\b', r'\bhow\b', r'\btell me\b', r'\bdescribe\b',
        r'\bwalk me through\b', r'\bhelp me understand\b', r'\bexplain\b',
        r'\bwhat\'s\b', r'\bwhat is\b', r'\bhow does\b', r'\bhow has\b',
        r'\bhow do\b', r'\bwhat does\b', r'\bwhat has\b', r'\bwhat would\b',
        r'\bwhat do\b', r'\bwhat are\b', r'\bwhat were\b', r'\bwhat might\b',
    ]
    has_open = any(re.search(p, text_lower) for p in open_patterns)

    if not has_open:
        return False, "no_open_question", (
            "⚠️ **Rule 2 broken — No open question found.** "
            "Your response needs a question that starts with 'What', 'How', or 'Tell me about...' "
            "to keep the farmer talking. A statement on its own won't do it."
        )

    # Rule 1: Must include some form of validation/acknowledgement
    # Check for empathy/validation keywords OR a reasonable length acknowledgement
    empathy_patterns = [
        r'\bunderstand\b', r'\bmakes sense\b', r'\bfair enough\b',
        r'\bappreciate\b', r'\btough\b', r'\bdifficult\b', r'\bhard\b',
        r'\bfrustrat\b', r'\bworry\b', r'\bconcern\b', r'\bright to\b',
        r'\bsounds like\b', r'\bseem(s)?\b', r'\bfeel(s)?\b',
        r'\bthat must\b', r'\bno wonder\b', r'\bcompletely\b',
        r'\bunderstandable\b', r'\btotally\b', r'\bof course\b',
        r'\bcan see why\b', r'\bcan understand\b', r'\bget that\b',
        r'\brespect\b', r'\bcredit\b', r'\bwhat you\'ve\b', r'\byears of\b',
        r'\bexperience\b', r'\bhistory\b', r'\bknow your\b',
    ]
    has_empathy = any(re.search(p, text_lower) for p in empathy_patterns)

    # Give benefit of the doubt if response is substantial (they tried to acknowledge something)
    # but only if it's long enough to plausibly contain validation
    if not has_empathy and len(text.split()) < 15:
        return False, "no_validation", (
            "⚠️ **Rule 1 broken — No validation found.** "
            "You went straight to a question without acknowledging what your farmer said first. "
            "They need to feel heard before they'll open up. Add a sentence that shows you understood their concern."
        )

    return True, None, "Good response — clear validation and an open question."


def is_warm_response(user_text):
    """Rough heuristic: was this a warm, empathetic response?"""
    text_lower = user_text.lower()
    warm_keywords = [
        "understand", "must be", "sounds like", "tough", "hard", "difficult",
        "that's fair", "fair enough", "appreciate", "respect", "credit",
        "no wonder", "completely", "totally", "of course", "can see",
        "feel", "frustrat", "worry", "concern", "experience", "know your"
    ]
    score = sum(1 for kw in warm_keywords if kw in text_lower)
    return score >= 2


def get_farmer_reply(scenario, layer_num, user_text, is_failure=False, attempt_num=1):
    """Get appropriate farmer reply based on context."""
    layer_data = scenario["layers"][layer_num]
    farmer_name = scenario["farmer_name"]

    if is_failure:
        if attempt_num == 1:
            return f"**{farmer_name}:** Look, like I said... {layer_data['text']}"
        else:
            return f"**{farmer_name}:** *(sighs)* I'm not sure you're quite hearing me. {layer_data['text']}"

    # Success — pick warm or cold reply based on quality of response
    warm = is_warm_response(user_text)
    replies = layer_data["warm_replies"] if warm else layer_data["cold_replies"]

    if replies:
        return f"**{farmer_name}:** {random.choice(replies)}"
    else:
        # Layer 5 — root cause reached
        return f"**{farmer_name}:** {layer_data['text']} ...If you can help me work through that, I suppose I'm open to hearing what options we actually have."


# --- SESSION STATE INIT ---
selected_key = st.selectbox("🎯 Choose a farming client scenario to practise:", list(SCENARIOS.keys()))
active_scenario = SCENARIOS[selected_key]
farmer_name = active_scenario["farmer_name"]

if "current_scenario_name" not in st.session_state or st.session_state.current_scenario_name != selected_key:
    st.session_state.current_scenario_name = selected_key
    st.session_state.layer = 1
    st.session_state.strikes = 0
    st.session_state.layer_attempts = 0
    st.session_state.total_strikes = 0
    st.session_state.scenarios_completed = 0
    st.session_state.layer_strike_log = {}  # {layer: strike_count}
    st.session_state.rules_broken_log = []  # list of rule names broken
    st.session_state.chat_history = [
        {"role": "farmer", "text": f"**{farmer_name}:** {active_scenario['layers'][1]['text']}"}
    ]
    st.session_state.coach_feedback = None
    st.session_state.game_over = False
    st.session_state.hint_shown = False

# --- MAIN UI ---
st.title("🚜 Farm Adviser Training Simulator")
st.subheader("Mastering the 5 Whys Through Open Questions")
st.write(
    "**Objective:** Guide your farmer from their surface objection down to the real root cause. "
    "Use **empathy first**, then **open questions**. No closed questions."
)
st.markdown("---")

# Progress indicator
current_layer = st.session_state.layer
total_layers = MAX_LAYERS
progress = (current_layer - 1) / (total_layers - 1) if total_layers > 1 else 0

col1, col2 = st.columns([3, 1])
with col1:
    st.progress(progress, text=f"Depth: Layer {current_layer} of {total_layers}")
with col2:
    strikes_display = ""
    for i in range(MAX_ATTEMPTS_PER_LAYER):
        if i < st.session_state.strikes:
            strikes_display += "🔴 "
        else:
            strikes_display += "⚪ "
    st.write(f"Attempts: {strikes_display}")

st.write(f"**Topic:** {active_scenario['topic']}")
st.markdown("---")

# Chat history
for message in st.session_state.chat_history:
    if message["role"] == "farmer":
        st.chat_message("user", avatar="👨‍🌾").write(message["text"])
    elif message["role"] == "adviser":
        st.chat_message("assistant", avatar="💼").write(message["text"])
    elif message["role"] == "coach":
        st.chat_message("assistant", avatar="🎓").error(message["text"])

# Coach feedback (shown once then cleared)
if st.session_state.coach_feedback:
    st.error(f"🎓 **Coach:** {st.session_state.coach_feedback}")
    st.session_state.coach_feedback = None

# --- GAME OVER / COMPLETION ---
if st.session_state.game_over:
    st.balloons()
    st.success(f"🎉 **Simulation complete!** You guided {farmer_name} to their root cause.")
    st.session_state.scenarios_completed = st.session_state.get("scenarios_completed", 0) + 1

    # End of session summary
    st.markdown("### 📊 Your Performance Summary")

    total_s = st.session_state.total_strikes
    if total_s == 0:
        rating = "🏆 Excellent — clean run, no mistakes"
        rating_color = "success"
    elif total_s <= 2:
        rating = "✅ Good — a couple of wobbles but you got there"
        rating_color = "success"
    elif total_s <= 5:
        rating = "⚠️ Fair — worth reviewing the rules before your next run"
        rating_color = "warning"
    else:
        rating = "❌ Needs work — focus on validation and open questions"
        rating_color = "error"

    st.info(f"**Overall:** {rating}")
    st.write(f"**Total strikes:** {total_s}")

    if st.session_state.layer_strike_log:
        st.write("**Strikes by layer:**")
        for layer_num, count in sorted(st.session_state.layer_strike_log.items()):
            bar = "🟥" * count + "⬜" * (MAX_ATTEMPTS_PER_LAYER - min(count, MAX_ATTEMPTS_PER_LAYER))
            st.write(f"Layer {layer_num}: {bar} ({count} strike{'s' if count != 1 else ''})")

    if st.session_state.rules_broken_log:
        from collections import Counter
        rule_counts = Counter(st.session_state.rules_broken_log)
        st.write("**Rules broken most often:**")
        rule_labels = {
            "closed_question": "Rule 3 — Closed questions",
            "no_open_question": "Rule 2 — Missing open question",
            "no_validation": "Rule 1 — No validation"
        }
        for rule, count in rule_counts.most_common():
            st.write(f"- {rule_labels.get(rule, rule)}: **{count}x**")
        # Targeted advice
        most_common = rule_counts.most_common(1)[0][0]
        if most_common == "closed_question":
            st.warning("**Focus area:** Practise rewriting your questions. Start every question with 'What' or 'How' and see if it still makes sense.")
        elif most_common == "no_open_question":
            st.warning("**Focus area:** Make sure every response ends with a question — and that it starts with 'What', 'How', or 'Tell me about...'")
        elif most_common == "no_validation":
            st.warning("**Focus area:** Before you ask anything, write one sentence that shows you heard what they said. That one habit changes everything.")

    if st.button("🔄 Run Again"):
        st.session_state.layer = 1
        st.session_state.strikes = 0
        st.session_state.layer_attempts = 0
        st.session_state.total_strikes = 0
        st.session_state.layer_strike_log = {}
        st.session_state.rules_broken_log = []
        st.session_state.chat_history = [
            {"role": "farmer", "text": f"**{farmer_name}:** {active_scenario['layers'][1]['text']}"}
        ]
        st.session_state.game_over = False
        st.rerun()

# --- INPUT HANDLING ---
elif user_input := st.chat_input(f"Your response to {farmer_name}..."):
    st.session_state.chat_history.append({"role": "adviser", "text": f"**You:** {user_input}"})
    st.session_state.layer_attempts += 1

    passed, rule_broken, feedback_msg = evaluate_response(user_input)

    if passed:
        # Reset strike/attempt counters for this layer
        st.session_state.strikes = 0
        st.session_state.layer_attempts = 0

        next_layer = st.session_state.layer + 1

        if next_layer > MAX_LAYERS:
            # Final layer reached
            farmer_reply = get_farmer_reply(active_scenario, MAX_LAYERS, user_input)
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            st.session_state.game_over = True
        else:
            farmer_reply = get_farmer_reply(active_scenario, st.session_state.layer, user_input)
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            st.session_state.layer = next_layer

    else:
        # Failed response
        st.session_state.strikes += 1
        st.session_state.total_strikes += 1

        # Log which rule was broken
        if rule_broken:
            st.session_state.rules_broken_log.append(rule_broken)
            # Track per layer
            layer_key = st.session_state.layer
            st.session_state.layer_strike_log[layer_key] = \
                st.session_state.layer_strike_log.get(layer_key, 0) + 1

        if st.session_state.strikes >= MAX_ATTEMPTS_PER_LAYER:
            # Max attempts reached — show hint and auto-advance
            hint = active_scenario["layers"][st.session_state.layer]["hint"]
            coach_msg = (
                f"{feedback_msg}\n\n"
                f"**Coach hint for this layer:** {hint}\n\n"
                f"*Moving you to the next layer so you can keep going.*"
            )
            st.session_state.chat_history.append({"role": "coach", "text": coach_msg})
            st.session_state.strikes = 0
            st.session_state.layer_attempts = 0

            # Auto-advance
            next_layer = st.session_state.layer + 1
            if next_layer > MAX_LAYERS:
                st.session_state.game_over = True
            else:
                farmer_reply = f"**{farmer_name}:** *(The conversation moves on...)* {active_scenario['layers'][next_layer]['text']}"
                st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
                st.session_state.layer = next_layer
        else:
            # Still has attempts left — show feedback and let them try again
            attempts_left = MAX_ATTEMPTS_PER_LAYER - st.session_state.strikes
            farmer_reply = get_farmer_reply(
                active_scenario,
                st.session_state.layer,
                user_input,
                is_failure=True,
                attempt_num=st.session_state.strikes
            )
            st.session_state.chat_history.append({"role": "farmer", "text": farmer_reply})
            st.session_state.chat_history.append({
                "role": "coach",
                "text": f"{feedback_msg}\n\n*You have {attempts_left} attempt{'s' if attempts_left != 1 else ''} left on this layer.*"
            })

    st.rerun()
