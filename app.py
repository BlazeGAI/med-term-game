import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Med Term Emergency!",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        margin: 5px 0;
    }
    .score-display {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
    }
    .patient-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        border: 4px solid #FFD700;
    }
    .timer-display {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .timer-warning {
        color: #FF4444;
        animation: pulse 1s infinite;
    }
    .timer-ok {
        color: #44FF44;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .streak-badge {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 10px 20px;
        border-radius: 25px;
        color: white;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        margin: 10px 0;
    }
    .question-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    h1 {
        text-align: center;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'
    st.session_state.current_patient = 0
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.lives = 3
    st.session_state.selected_answer = None
    st.session_state.time_left = 30
    st.session_state.question_start_time = None
    st.session_state.max_streak = 0

# Patient data
patients = [
    {
        "name": "Marcus Williams",
        "age": 52,
        "sprite": "👨‍🦲",
        "condition": "Stroke Alert",
        "story": "Lost feeling in right arm, speech slurred, family called 911...",
        "questions": [
            {
                "q": "Patient has 'hemiparesis' on right side. What does this mean?",
                "options": ["Complete paralysis", "Weakness on one side", "Numbness", "Tremors"],
                "correct": 1,
                "points": 100,
            },
            {
                "q": "Speech difficulty is called 'dysphasia'. What system is affected?",
                "options": ["Motor nerves", "Sensory nerves", "Language centers in brain", "Spinal cord"],
                "correct": 2,
                "points": 150,
            },
            {
                "q": "CT scan shows 'ischemia'. What happened to brain tissue?",
                "options": ["Bleeding", "Reduced blood flow", "Swelling", "Infection"],
                "correct": 1,
                "points": 150,
            }
        ]
    },
    {
        "name": "Sophia Chen",
        "age": 34,
        "sprite": "👩‍🦱",
        "condition": "Vision Emergency",
        "story": "Sudden vision loss in left eye, seeing flashing lights...",
        "questions": [
            {
                "q": "Patient reports 'photopsia'. What are they experiencing?",
                "options": ["Double vision", "Blind spots", "Flashing lights", "Color blindness"],
                "correct": 2,
                "points": 150,
            },
            {
                "q": "Doctor examines the 'optic nerve'. What does it connect?",
                "options": ["Eye to brain", "Ears to brain", "Nose to brain", "Tongue to brain"],
                "correct": 0,
                "points": 100,
            },
            {
                "q": "Diagnosed with 'scotoma'. What is this?",
                "options": ["Swollen eyelid", "Blind spot in vision", "Eye infection", "Blurry vision"],
                "correct": 1,
                "points": 150,
            }
        ]
    },
    {
        "name": "David Kumar",
        "age": 41,
        "sprite": "👨‍🦳",
        "condition": "Seizure Activity",
        "story": "Collapsed at work, jerking movements, unresponsive...",
        "questions": [
            {
                "q": "Witnesses describe 'tonic-clonic' seizure. What happened?",
                "options": ["Brief staring spell", "Stiffening then jerking", "Only tremors", "Fainting only"],
                "correct": 1,
                "points": 150,
            },
            {
                "q": "After seizure, patient has 'postictal' confusion. When is this?",
                "options": ["Before seizure", "During seizure", "After seizure", "Between seizures"],
                "correct": 2,
                "points": 100,
            },
            {
                "q": "EEG measures brain's what?",
                "options": ["Blood flow", "Oxygen levels", "Electrical activity", "Temperature"],
                "correct": 2,
                "points": 100,
            }
        ]
    },
    {
        "name": "Isabella Torres",
        "age": 67,
        "sprite": "👵",
        "condition": "Nerve Pain Syndrome",
        "story": "Burning pain in feet, numbness in hands, diabetes history...",
        "questions": [
            {
                "q": "Diagnosed with 'peripheral neuropathy'. What's affected?",
                "options": ["Brain only", "Spinal cord", "Nerves in extremities", "Central nervous system"],
                "correct": 2,
                "points": 150,
            },
            {
                "q": "Patient has 'paresthesia' in fingers. What does she feel?",
                "options": ["Pain", "Tingling/pins & needles", "Weakness", "Stiffness"],
                "correct": 1,
                "points": 150,
            },
            {
                "q": "Loss of sensation is called what?",
                "options": ["Analgesia", "Anesthesia", "Hyperesthesia", "Dysesthesia"],
                "correct": 1,
                "points": 100,
            }
        ]
    },
    {
        "name": "Michael Jackson",
        "age": 29,
        "sprite": "👨",
        "condition": "Hearing Crisis",
        "story": "Sudden ringing in ears, dizziness, room spinning...",
        "questions": [
            {
                "q": "Patient has 'tinnitus'. What symptom is this?",
                "options": ["Hearing loss", "Ringing in ears", "Ear pain", "Fluid drainage"],
                "correct": 1,
                "points": 100,
            },
            {
                "q": "Experiencing 'vertigo'. What does patient feel?",
                "options": ["Headache", "Nausea only", "Spinning sensation", "Blurred vision"],
                "correct": 2,
                "points": 150,
            },
            {
                "q": "Doctor tests 'vestibular' function. What's being checked?",
                "options": ["Hearing", "Balance and spatial orientation", "Smell", "Taste"],
                "correct": 1,
                "points": 150,
            }
        ]
    }
]

def start_game():
    st.session_state.game_state = 'playing'
    st.session_state.current_patient = 0
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.lives = 3
    st.session_state.selected_answer = None
    st.session_state.time_left = 30
    st.session_state.question_start_time = time.time()
    st.session_state.max_streak = 0

def handle_answer(answer_index):
    if st.session_state.selected_answer is not None:
        return
    
    st.session_state.selected_answer = answer_index
    patient = patients[st.session_state.current_patient]
    question = patient['questions'][st.session_state.current_question]
    
    # Calculate time taken
    time_taken = time.time() - st.session_state.question_start_time
    time_remaining = max(0, 30 - int(time_taken))
    
    if answer_index == question['correct']:
        # Correct answer
        time_bonus = time_remaining * 2
        streak_bonus = st.session_state.streak * 50
        total_points = question['points'] + time_bonus + streak_bonus
        st.session_state.score += total_points
        st.session_state.streak += 1
        st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
    else:
        # Wrong answer
        st.session_state.lives -= 1
        st.session_state.streak = 0
        if st.session_state.lives <= 0:
            st.session_state.game_state = 'game_over'

def next_question():
    patient = patients[st.session_state.current_patient]
    
    if st.session_state.current_question < len(patient['questions']) - 1:
        st.session_state.current_question += 1
    elif st.session_state.current_patient < len(patients) - 1:
        st.session_state.current_patient += 1
        st.session_state.current_question = 0
    else:
        st.session_state.game_state = 'victory'
    
    st.session_state.selected_answer = None
    st.session_state.time_left = 30
    st.session_state.question_start_time = time.time()

# Menu Screen
if st.session_state.game_state == 'menu':
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='font-size: 72px; margin-bottom: 0;'>🏥 MED TERM</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #FF1493; font-size: 48px;'>EMERGENCY!</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(0,0,0,0.7); padding: 30px; border-radius: 15px; margin: 30px 0;'>
            <h3 style='text-align: center; color: white; font-size: 28px;'>🚨 5 Patients Need Your Help! 🚨</h3>
            <p style='text-align: center; color: #DDD; font-size: 20px;'>Answer neurological & sensory questions</p>
            <p style='text-align: center; color: #DDD; font-size: 20px;'>⏱️ Beat the clock for bonus points</p>
            <p style='text-align: center; color: #DDD; font-size: 20px;'>❤️ Don't lose all 3 lives!</p>
            <p style='text-align: center; color: #FFD700; font-size: 22px; margin-top: 20px;'>🔥 Build combos for huge scores!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 START GAME", key="start_btn", type="primary"):
            start_game()
            st.rerun()

# Game Over Screen
elif st.session_state.game_state == 'game_over':
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='font-size: 72px; color: #FF4444; text-align: center;'>💀 GAME OVER</h1>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: rgba(0,0,0,0.8); padding: 40px; border-radius: 15px; margin: 30px 0;'>
            <h3 style='text-align: center; color: white; font-size: 36px;'>Final Score</h3>
            <div class='score-display'>{st.session_state.score}</div>
            <p style='text-align: center; color: #AAA; font-size: 20px; margin-top: 20px;'>
                You saved {st.session_state.current_patient} patient{'s' if st.session_state.current_patient != 1 else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 TRY AGAIN", key="retry_btn", type="primary"):
            start_game()
            st.rerun()

# Victory Screen
elif st.session_state.game_state == 'victory':
    score = st.session_state.score
    rank = "MASTER PHYSICIAN" if score > 2500 else "EXPERT DOCTOR" if score > 2000 else "SKILLED MEDIC" if score > 1500 else "CERTIFIED INTERN"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='font-size: 72px; color: #FFD700; text-align: center;'>🏆 VICTORY!</h1>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: rgba(0,0,0,0.7); padding: 40px; border-radius: 15px; margin: 30px 0;'>
            <h3 style='text-align: center; color: #FFD700; font-size: 32px;'>⭐ {rank} ⭐</h3>
            <div class='score-display'>{score}</div>
            <div style='margin-top: 30px;'>
                <div style='display: flex; justify-content: space-between; color: white; font-size: 18px; margin: 10px 0;'>
                    <span>Patients Saved:</span>
                    <span style='color: #44FF44; font-weight: bold;'>5/5</span>
                </div>
                <div style='display: flex; justify-content: space-between; color: white; font-size: 18px; margin: 10px 0;'>
                    <span>Best Streak:</span>
                    <span style='color: #FF6B35; font-weight: bold;'>{st.session_state.max_streak}🔥</span>
                </div>
                <div style='display: flex; justify-content: space-between; color: white; font-size: 18px; margin: 10px 0;'>
                    <span>Lives Remaining:</span>
                    <span style='color: #FF4444; font-weight: bold;'>{'❤️' * st.session_state.lives}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 PLAY AGAIN", key="play_again_btn", type="primary"):
            start_game()
            st.rerun()

# Playing Screen
elif st.session_state.game_state == 'playing':
    patient = patients[st.session_state.current_patient]
    question = patient['questions'][st.session_state.current_question]
    
    # Calculate progress
    total_questions = sum(len(p['questions']) for p in patients)
    questions_answered = sum(len(patients[i]['questions']) for i in range(st.session_state.current_patient)) + st.session_state.current_question
    progress = questions_answered / total_questions
    
    # Calculate time remaining
    if st.session_state.question_start_time:
        time_elapsed = time.time() - st.session_state.question_start_time
        time_remaining = max(0, 30 - int(time_elapsed))
    else:
        time_remaining = 30
    
    # Check for timeout
    if time_remaining <= 0 and st.session_state.selected_answer is None:
        st.session_state.lives -= 1
        st.session_state.streak = 0
        if st.session_state.lives <= 0:
            st.session_state.game_state = 'game_over'
            st.rerun()
        else:
            next_question()
            st.rerun()
    
    # HUD
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"<div style='background: rgba(0,0,0,0.7); padding: 15px; border-radius: 25px; text-align: center;'><span style='color: #FFD700; font-size: 32px; font-weight: bold;'>⭐ {st.session_state.score}</span></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div style='background: rgba(0,0,0,0.7); padding: 15px; border-radius: 25px; text-align: center;'><span style='color: #FF4444; font-size: 32px;'>{'❤️ ' * st.session_state.lives}</span></div>", unsafe_allow_html=True)
    
    if st.session_state.streak > 0:
        st.markdown(f"<div class='streak-badge'>🔥 {st.session_state.streak} STREAK!</div>", unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress)
    
    # Patient Card
    st.markdown(f"""
    <div class='patient-card'>
        <div style='display: flex; align-items: center; gap: 20px; margin-bottom: 20px;'>
            <div style='font-size: 80px;'>{patient['sprite']}</div>
            <div>
                <h2 style='margin: 0; font-size: 36px;'>{patient['name']}</h2>
                <p style='margin: 5px 0; color: #FFD700; font-size: 20px;'>Age: {patient['age']}</p>
                <p style='margin: 5px 0; color: #FF6B6B; font-size: 22px; font-weight: bold;'>{patient['condition']}</p>
            </div>
        </div>
        <div style='background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px;'>
            <p style='margin: 0; font-style: italic; font-size: 18px;'>{patient['story']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer
    timer_class = "timer-warning" if time_remaining <= 10 else "timer-ok"
    st.markdown(f"""
    <div style='background: rgba(0,0,0,0.7); padding: 20px; border-radius: 15px; margin: 20px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='color: white; font-weight: bold; font-size: 24px;'>TIME</span>
            <span class='timer-display {timer_class}'>{time_remaining}s</span>
        </div>
        <div style='background: #444; height: 15px; border-radius: 10px; margin-top: 10px; overflow: hidden;'>
            <div style='background: {"#FF4444" if time_remaining <= 10 else "#44FF44"}; height: 100%; width: {(time_remaining/30)*100}%; transition: width 1s linear;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question
    st.markdown(f"""
    <div class='question-box'>
        <h3 style='color: #333; font-size: 28px; margin-bottom: 30px;'>{question['q']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    for i, option in enumerate(question['options']):
        is_correct = i == question['correct']
        is_selected = i == st.session_state.selected_answer
        
        if st.session_state.selected_answer is not None:
            if is_selected and is_correct:
                button_type = "primary"
                emoji = " ✓"
            elif is_selected and not is_correct:
                button_type = "secondary"
                emoji = " ✗"
            elif is_correct:
                button_type = "primary"
                emoji = " ✓"
            else:
                button_type = "secondary"
                emoji = ""
            
            st.button(
                f"{option}{emoji}",
                key=f"option_{i}",
                disabled=True,
                type=button_type,
                use_container_width=True
            )
        else:
            if st.button(option, key=f"option_{i}", use_container_width=True):
                handle_answer(i)
                st.rerun()
    
    # Next button
    if st.session_state.selected_answer is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➡️ NEXT", key="next_btn", type="primary", use_container_width=True):
            next_question()
            st.rerun()
    
    # Auto-refresh for timer
    if st.session_state.selected_answer is None:
        time.sleep(0.5)
        st.rerun()
