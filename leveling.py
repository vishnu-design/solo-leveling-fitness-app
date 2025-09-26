import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import random

# Configure Streamlit page
st.set_page_config(
    page_title="🏋️ Solo Leveling Fitness System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Solo Leveling theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.main {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    font-family: 'Orbitron', monospace;
}

.stMetric {
    background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3a 100%);
    border: 2px solid #ff6b35;
    border-radius: 15px;
    padding: 20px;
}

.stMetric > div {
    color: #fff !important;
}

.metric-container {
    background: linear-gradient(135deg, #2a2a3a, #1e1e2e);
    border: 2px solid #ff6b35;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
}

.level-header {
    background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcd3c);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3em;
    font-weight: 900;
    text-align: center;
    margin-bottom: 20px;
}

.quest-complete {
    background: linear-gradient(45deg, #00ff88, #00cc6a);
    color: black !important;
    font-weight: bold;
}

.legendary-quest {
    border: 3px solid #ffcd3c !important;
    background: linear-gradient(135deg, rgba(255, 205, 60, 0.1), rgba(255, 107, 53, 0.1));
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'hunter_data' not in st.session_state:
        st.session_state.hunter_data = {
            'level': 1,
            'xp': 0,
            'total_xp': 0,
            'workouts_completed': 0,
            'exercises_completed': 0,
            'days_active': 0,
            'streak': 0,
            'current_weight': 78.7,
            'body_fat': 29.2,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'last_active': None
        }
    
    if 'nutrition_data' not in st.session_state:
        st.session_state.nutrition_data = {
            'daily_calories': 0,
            'daily_protein': 0,
            'daily_carbs': 0,
            'daily_fats': 0,
            'food_log': [],
            'last_reset': datetime.now().date()
        }
    
    if 'workout_data' not in st.session_state:
        st.session_state.workout_data = {
            'tuesday_pull': {'completed': False, 'exercises': []},
            'wednesday_push': {'completed': False, 'exercises': []},
            'thursday_legs': {'completed': False, 'exercises': []},
            'friday_push': {'completed': False, 'exercises': []},
            'saturday_pull_legendary': {'completed': False, 'exercises': []},
            'sunday_legs': {'completed': False, 'exercises': []},
            'last_reset': datetime.now().date()
        }
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = {
            'first_workout': False,
            'week_streak': False,
            'month_streak': False,
            'first_pullup': False,
            'level_10': False,
            'shredded_goal': False
        }

def calculate_xp_for_level(level):
    return level * 1000

def check_level_up():
    current_level = st.session_state.hunter_data['level']
    current_xp = st.session_state.hunter_data['xp']
    xp_needed = calculate_xp_for_level(current_level)
    
    if current_xp >= xp_needed:
        st.session_state.hunter_data['level'] += 1
        st.session_state.hunter_data['xp'] = current_xp - xp_needed
        return True
    return False

def add_xp(amount):
    st.session_state.hunter_data['xp'] += amount
    st.session_state.hunter_data['total_xp'] += amount
    
    if check_level_up():
        st.success(f"🎉 LEVEL UP! You are now Hunter Level {st.session_state.hunter_data['level']}!")
        st.balloons()

def reset_daily_data():
    today = datetime.now().date()
    
    # Reset nutrition data if it's a new day
    if st.session_state.nutrition_data['last_reset'] != today:
        st.session_state.nutrition_data.update({
            'daily_calories': 0,
            'daily_protein': 0,
            'daily_carbs': 0,
            'daily_fats': 0,
            'food_log': [],
            'last_reset': today
        })
    
    # Reset workout data if it's a new week (Monday)
    if today.weekday() == 0 and st.session_state.workout_data['last_reset'] != today:
        for day in st.session_state.workout_data:
            if day != 'last_reset':
                st.session_state.workout_data[day] = {'completed': False, 'exercises': []}
        st.session_state.workout_data['last_reset'] = today

def main():
    initialize_session_state()
    reset_daily_data()
    display_sidebar()
    
    # Header
    st.markdown('<h1 class="level-header">⚡ HUNTER FITNESS SYSTEM ⚡</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #ffcd3c; font-size: 1.2em;">Solo Leveling: Path to Shredded Awakening</p>', unsafe_allow_html=True)
    
    # Hunter Status Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        level = st.session_state.hunter_data['level']
        st.metric("🔥 Hunter Level", f"Level {level}")
        
        current_xp = st.session_state.hunter_data['xp']
        xp_needed = calculate_xp_for_level(level)
        xp_progress = min(current_xp / xp_needed * 100, 100)
        
        st.progress(xp_progress / 100)
        st.write(f"XP: {current_xp:,} / {xp_needed:,}")
    
    with col2:
        st.metric("📊 Body Fat", f"{st.session_state.hunter_data['body_fat']:.1f}%", "Target: 10-12%")
        fat_progress = max(0, (29.2 - st.session_state.hunter_data['body_fat']) / (29.2 - 11) * 100)
        st.progress(fat_progress / 100)
    
    with col3:
        st.metric("⚖️ Current Weight", f"{st.session_state.hunter_data['current_weight']:.1f}kg", "Target: 62-65kg")
        weight_lost = 78.7 - st.session_state.hunter_data['current_weight']
        st.write(f"Lost: {weight_lost:.1f}kg")
    
    with col4:
        st.metric("📅 Days Active", st.session_state.hunter_data['days_active'])
        st.metric("🔥 Streak", f"{st.session_state.hunter_data['streak']} days")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⚔️ Daily Quests", "🍎 Nutrition System", "📊 Hunter Stats", "🏆 Achievements"])
    
    with tab1:
        display_workout_system()
    
    with tab2:
        display_nutrition_system()
        display_meal_suggestions()
    
    with tab3:
        display_stats_dashboard()
    
    with tab4:
        display_achievements()

def display_workout_system():
    st.header("⚔️ WEEKLY DUNGEON RAIDS ⚔️")
    
    # Workout schedule
    workout_schedule = {
        'Monday': {'type': 'rest', 'name': '😴 REST DAY', 'xp': 0, 'exercises': []},
        'Tuesday': {
            'type': 'pull', 
            'name': '🗡️ PULL QUEST (No Assisted Pull-ups)', 
            'xp': 150,
            'exercises': [
                {'name': 'Lat Pulldowns', 'sets': 4, 'reps': '8-12', 'rest': '90s', 'xp': 30},
                {'name': 'Cable Rows', 'sets': 4, 'reps': '8-12', 'rest': '90s', 'xp': 30},
                {'name': 'Cable Bicep Curls', 'sets': 3, 'reps': '10-15', 'rest': '60s', 'xp': 25},
                {'name': 'Reverse Grip Curls', 'sets': 3, 'reps': '12-15', 'rest': '60s', 'xp': 20}
            ]
        },
        'Wednesday': {
            'type': 'push', 
            'name': '🛡️ PUSH QUEST', 
            'xp': 150,
            'exercises': [
                {'name': 'Chest Press', 'sets': 4, 'reps': '8-12', 'rest': '90s', 'xp': 35},
                {'name': 'Shoulder Press Machine', 'sets': 4, 'reps': '8-12', 'rest': '90s', 'xp': 30},
                {'name': 'Tricep Pulldowns', 'sets': 3, 'reps': '10-15', 'rest': '60s', 'xp': 25},
                {'name': 'Push-ups (Progression)', 'sets': 2, 'reps': 'Max', 'rest': '60s', 'xp': 20}
            ]
        },
        'Thursday': {
            'type': 'legs', 
            'name': '🦵 LEG QUEST + CORE', 
            'xp': 200,
            'exercises': [
                {'name': 'Leg Press', 'sets': 4, 'reps': '12-20', 'rest': '2min', 'xp': 50},
                {'name': 'Seated Calf Raises', 'sets': 4, 'reps': '15-20', 'rest': '60s', 'xp': 25},
                {'name': 'Plank Hold', 'sets': 3, 'reps': '30-60s', 'rest': '60s', 'xp': 30},
                {'name': 'Kettlebell Swings', 'sets': 3, 'reps': '15-20', 'rest': '90s', 'xp': 35}
            ]
        },
        'Friday': {
            'type': 'push', 
            'name': '🛡️ PUSH QUEST (Repeat)', 
            'xp': 150,
            'exercises': [
                {'name': 'Same as Wednesday', 'sets': '-', 'reps': '-', 'rest': '-', 'xp': 110}
            ]
        },
        'Saturday': {
            'type': 'legendary', 
            'name': '🔥 LEGENDARY PULL QUEST (Assisted Pull-ups!)', 
            'xp': 250,
            'exercises': [
                {'name': '🏆 ASSISTED PULL-UPS (LEGENDARY)', 'sets': 4, 'reps': '5-8', 'rest': '2min', 'xp': 100},
                {'name': 'Lat Pulldowns (Light)', 'sets': 3, 'reps': '8-12', 'rest': '90s', 'xp': 25},
                {'name': 'Cable Bicep Curls', 'sets': 3, 'reps': '10-15', 'rest': '60s', 'xp': 25}
            ]
        },
        'Sunday': {
            'type': 'legs', 
            'name': '🦵 LEG QUEST + CORE (Repeat)', 
            'xp': 200,
            'exercises': [
                {'name': 'Same as Thursday', 'sets': '-', 'reps': '-', 'rest': '-', 'xp': 140}
            ]
        }
    }
    
    # Display current day's workout
    today = datetime.now().strftime('%A')
    current_workout = workout_schedule[today]
    
    st.subheader(f"🎯 Today's Quest: {current_workout['name']}")
    
    if current_workout['type'] != 'rest':
        quest_key = f"{today.lower()}_{current_workout['type']}"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Total XP Available:** {current_workout['xp']} XP")
        with col2:
            if st.button(f"Complete {today}'s Quest!", type="primary"):
                if not st.session_state.workout_data.get(quest_key, {}).get('completed', False):
                    add_xp(current_workout['xp'])
                    st.session_state.workout_data[quest_key] = {'completed': True, 'exercises': []}
                    st.session_state.hunter_data['workouts_completed'] += 1
                    st.success(f"🎉 Quest Complete! +{current_workout['xp']} XP earned!")
                else:
                    st.warning("Quest already completed today!")
        
        # Exercise breakdown
        st.write("**Quest Objectives:**")
        for i, exercise in enumerate(current_workout['exercises']):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                if exercise['name'].startswith('🏆'):
                    st.markdown(f"**{exercise['name']}**", help="Legendary Exercise!")
                else:
                    st.write(f"**{exercise['name']}**")
            
            with col2:
                st.write(f"{exercise['sets']} sets")
            
            with col3:
                st.write(f"{exercise['reps']} reps")
            
            with col4:
                st.write(f"{exercise['rest']} rest")
            
            with col5:
                exercise_key = f"{quest_key}_{i}"
                if st.button("✅", key=f"complete_{exercise_key}"):
                    if exercise_key not in st.session_state.workout_data.get(quest_key, {}).get('exercises', []):
                        add_xp(exercise['xp'])
                        if quest_key not in st.session_state.workout_data:
                            st.session_state.workout_data[quest_key] = {'completed': False, 'exercises': []}
                        st.session_state.workout_data[quest_key]['exercises'].append(exercise_key)
                        st.session_state.hunter_data['exercises_completed'] += 1
                        st.success(f"+{exercise['xp']} XP!")
    else:
        st.info("🛌 Rest day! Your body grows stronger during recovery. Take this time to plan your nutrition and prepare for tomorrow's quest!")
        
        if st.button("Log Rest Day"):
            add_xp(50)  # Small XP for consistency
            st.success("🎉 Rest day logged! +50 XP for consistency!")
    
    # Weekly overview
    st.subheader("📅 Weekly Quest Overview")
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    progress_data = []
    
    for day in days:
        workout = workout_schedule[day]
        quest_key = f"{day.lower()}_{workout['type']}"
        completed = st.session_state.workout_data.get(quest_key, {}).get('completed', False)
        progress_data.append({
            'Day': day,
            'Quest': workout['name'],
            'XP': workout['xp'],
            'Status': '✅ Complete' if completed else '⏳ Pending',
            'Type': workout['type']
        })
    
    df_progress = pd.DataFrame(progress_data)
    st.dataframe(df_progress, use_container_width=True)

def display_nutrition_system():
    st.header("🍎 HUNTER NUTRITION SYSTEM 🍎")
    
    # Nutrition targets
    targets = {
        'calories': 1790,
        'protein': 157,
        'carbs': 179,
        'fats': 50
    }
    
    # Current nutrition status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        calorie_progress = min(st.session_state.nutrition_data['daily_calories'] / targets['calories'] * 100, 100)
        st.metric("🔥 Calories", f"{st.session_state.nutrition_data['daily_calories']:.0f}", f"Target: {targets['calories']}")
        st.progress(calorie_progress / 100)
    
    with col2:
        protein_progress = min(st.session_state.nutrition_data['daily_protein'] / targets['protein'] * 100, 100)
        st.metric("🥩 Protein", f"{st.session_state.nutrition_data['daily_protein']:.1f}g", f"Target: {targets['protein']}g")
        st.progress(protein_progress / 100)
    
    with col3:
        carbs_progress = min(st.session_state.nutrition_data['daily_carbs'] / targets['carbs'] * 100, 100)
        st.metric("🍞 Carbs", f"{st.session_state.nutrition_data['daily_carbs']:.1f}g", f"Target: {targets['carbs']}g")
        st.progress(carbs_progress / 100)
    
    with col4:
        fats_progress = min(st.session_state.nutrition_data['daily_fats'] / targets['fats'] * 100, 100)
        st.metric("🥑 Fats", f"{st.session_state.nutrition_data['daily_fats']:.1f}g", f"Target: {targets['fats']}g")
        st.progress(fats_progress / 100)
    
    # Food logging
    st.subheader("📝 Log Food Intake")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("food_form"):
            food_name = st.text_input("Food Item", placeholder="e.g., Chicken Breast, Rice")
            
            col_cal, col_pro, col_car, col_fat = st.columns(4)
            with col_cal:
                calories = st.number_input("Calories", min_value=0, step=1)
            with col_pro:
                protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
            with col_car:
                carbs = st.number_input("Carbs (g)", min_value=0.0, step=0.1)
            with col_fat:
                fats = st.number_input("Fats (g)", min_value=0.0, step=0.1)
            
            submitted = st.form_submit_button("Add Food (+10 XP)", type="primary")
            
            if submitted and food_name:
                # Add to nutrition totals
                st.session_state.nutrition_data['daily_calories'] += calories
                st.session_state.nutrition_data['daily_protein'] += protein
                st.session_state.nutrition_data['daily_carbs'] += carbs
                st.session_state.nutrition_data['daily_fats'] += fats
                
                # Add to food log
                food_entry = {
                    'name': food_name,
                    'calories': calories,
                    'protein': protein,
                    'carbs': carbs,
                    'fats': fats,
                    'time': datetime.now().strftime('%H:%M')
                }
                st.session_state.nutrition_data['food_log'].append(food_entry)
                
                # Add XP
                add_xp(10)
                st.success(f"✅ {food_name} logged! +10 XP")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Today's Log", type="secondary"):
            st.session_state.nutrition_data.update({
                'daily_calories': 0,
                'daily_protein': 0,
                'daily_carbs': 0,
                'daily_fats': 0,
                'food_log': []
            })
            st.success("Food log cleared!")
            st.rerun()
    
    # Food log display
    if st.session_state.nutrition_data['food_log']:
        st.subheader("📋 Today's Food Log")
        
        food_df = pd.DataFrame(st.session_state.nutrition_data['food_log'])
        st.dataframe(food_df, use_container_width=True)
        
        # Macro breakdown chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Progress towards targets
            progress_data = {
                'Macro': ['Calories', 'Protein', 'Carbs', 'Fats'],
                'Current': [
                    st.session_state.nutrition_data['daily_calories'],
                    st.session_state.nutrition_data['daily_protein'],
                    st.session_state.nutrition_data['daily_carbs'],
                    st.session_state.nutrition_data['daily_fats']
                ],
                'Target': [targets['calories'], targets['protein'], targets['carbs'], targets['fats']]
            }
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Current', x=progress_data['Macro'], y=progress_data['Current'], marker_color='#ff6b35'))
            fig.add_trace(go.Bar(name='Target', x=progress_data['Macro'], y=progress_data['Target'], marker_color='#ffcd3c'))
            fig.update_layout(title="Macro Progress", barmode='group', template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Calorie breakdown pie chart
            macro_calories = {
                'Protein': st.session_state.nutrition_data['daily_protein'] * 4,
                'Carbs': st.session_state.nutrition_data['daily_carbs'] * 4,
                'Fats': st.session_state.nutrition_data['daily_fats'] * 9
            }
            
            if sum(macro_calories.values()) > 0:
                fig = px.pie(
                    values=list(macro_calories.values()),
                    names=list(macro_calories.keys()),
                    title="Calorie Distribution",
                    color_discrete_sequence=['#ff6b35', '#ffcd3c', '#00ff88']
                )
                fig.update_layout(template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)

def display_stats_dashboard():
    st.header("📊 HUNTER TRANSFORMATION STATS 📊")
    
    # Key statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💪 Total Workouts", st.session_state.hunter_data['workouts_completed'])
    
    with col2:
        st.metric("🎯 Exercises Done", st.session_state.hunter_data['exercises_completed'])
    
    with col3:
        st.metric("⚡ Total XP", f"{st.session_state.hunter_data['total_xp']:,}")
    
    with col4:
        estimated_fat_loss = (st.session_state.hunter_data['total_xp'] / 1000) * 0.1  # Rough estimation
        st.metric("🔥 Est. Fat Loss", f"{estimated_fat_loss:.1f}kg")
    
    # Progress tracking
    st.subheader("📈 Transformation Timeline")
    
    # Calculate days since start
    start_date = datetime.strptime(st.session_state.hunter_data['start_date'], '%Y-%m-%d')
    days_elapsed = (datetime.now() - start_date).days
    days_remaining = max(0, 180 - days_elapsed)  # 6 months = ~180 days
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **🎯 Transformation Timeline**
        - **Current Status:** Hunter Level {st.session_state.hunter_data['level']} - {"Beginning Awakening" if st.session_state.hunter_data['level'] < 5 else "Rapid Progress" if st.session_state.hunter_data['level'] < 15 else "Elite Hunter"}
        - **Days Elapsed:** {days_elapsed} days
        - **Days Remaining:** {days_remaining} days
        - **Target Body Fat:** 10-12%
        - **Estimated Completion:** 6-8 months
        """)
    
    with col2:
        # Level progression chart
        level_data = {
            'Level': list(range(1, st.session_state.hunter_data['level'] + 5)),
            'XP Required': [calculate_xp_for_level(i) for i in range(1, st.session_state.hunter_data['level'] + 5)],
            'Status': ['Completed' if i < st.session_state.hunter_data['level'] 
                      else 'Current' if i == st.session_state.hunter_data['level'] 
                      else 'Future' for i in range(1, st.session_state.hunter_data['level'] + 5)]
        }
        
        fig = px.bar(
            pd.DataFrame(level_data),
            x='Level',
            y='XP Required',
            color='Status',
            title="Level Progression",
            color_discrete_map={'Completed': '#00ff88', 'Current': '#ff6b35', 'Future': '#666'}
        )
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    # Weight and body fat tracking
    st.subheader("⚖️ Body Composition Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight update
        new_weight = st.number_input(
            "Update Current Weight (kg)",
            min_value=50.0,
            max_value=120.0,
            value=st.session_state.hunter_data['current_weight'],
            step=0.1
        )
        
        if st.button("Update Weight"):
            st.session_state.hunter_data['current_weight'] = new_weight
            st.success("Weight updated!")
    
    with col2:
        # Body fat update
        new_body_fat = st.number_input(
            "Update Body Fat %",
            min_value=5.0,
            max_value=40.0,
            value=st.session_state.hunter_data['body_fat'],
            step=0.1
        )
        
        if st.button("Update Body Fat"):
            st.session_state.hunter_data['body_fat'] = new_body_fat
            st.success("Body fat updated!")

def display_achievements():
    st.header("🏆 HUNTER ACHIEVEMENTS 🏆")
    
    achievements = {
        'first_workout': {
            'name': '🎯 First Quest Complete',
            'description': 'Complete your first workout',
            'condition': st.session_state.hunter_data['workouts_completed'] >= 1,
            'xp_reward': 100
        },
        'week_streak': {
            'name': '🔥 Week Warrior',
            'description': 'Maintain a 7-day streak',
            'condition': st.session_state.hunter_data['streak'] >= 7,
            'xp_reward': 500
        },
        'month_streak': {
            'name': '⚡ Monthly Master',
            'description': 'Maintain a 30-day streak',
            'condition': st.session_state.hunter_data['streak'] >= 30,
            'xp_reward': 2000
        },
        'first_pullup': {
            'name': '💪 Pull-up Pioneer',
            'description': 'Complete 10 assisted pull-up sessions',
            'condition': st.session_state.hunter_data['exercises_completed'] >= 40,  # Rough estimate
            'xp_reward': 750
        },
        'level_10': {
            'name': '🌟 Elite Hunter',
            'description': 'Reach Hunter Level 10',
            'condition': st.session_state.hunter_data['level'] >= 10,
            'xp_reward': 1000
        },
        'shredded_goal': {
            'name': '🏆 Shredded Awakening',
            'description': 'Reach 12% body fat or lower',
            'condition': st.session_state.hunter_data['body_fat'] <= 12.0,
            'xp_reward': 5000
        }
    }
    
    for achievement_key, achievement in achievements.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if achievement['condition']:
                if not st.session_state.achievements[achievement_key]:
                    # Achievement just unlocked!
                    st.session_state.achievements[achievement_key] = True
                    add_xp(achievement['xp_reward'])
                    st.success(f"🎉 Achievement Unlocked: {achievement['name']}! +{achievement['xp_reward']} XP!")
                
                st.success(f"✅ **{achievement['name']}** - {achievement['description']}")
            else:
                st.info(f"🔒 **{achievement['name']}** - {achievement['description']}")
        
        with col2:
            st.write(f"**{achievement['xp_reward']} XP**")
        
        with col3:
            if achievement['condition']:
                st.write("**UNLOCKED**")
            else:
                st.write("*Locked*")
    
    # Achievement progress summary
    unlocked = sum(1 for key in achievements if st.session_state.achievements[key])
    total = len(achievements)
    
    st.subheader(f"🏅 Achievement Progress: {unlocked}/{total}")
    st.progress(unlocked / total)
    
    if unlocked == total:
        st.balloons()
        st.success("🏆 LEGENDARY HUNTER STATUS ACHIEVED! You have unlocked all achievements!")

def save_data():
    """Save session state to JSON file"""
    data_to_save = {
        'hunter_data': st.session_state.hunter_data,
        'nutrition_data': st.session_state.nutrition_data,
        'workout_data': st.session_state.workout_data,
        'achievements': st.session_state.achievements
    }
    
    # Convert datetime objects to strings
    data_to_save['nutrition_data']['last_reset'] = str(data_to_save['nutrition_data']['last_reset'])
    data_to_save['workout_data']['last_reset'] = str(data_to_save['workout_data']['last_reset'])
    
    return json.dumps(data_to_save, indent=2)

def load_data(json_data):
    """Load data from JSON"""
    try:
        data = json.loads(json_data)
        
        # Convert string dates back to date objects
        data['nutrition_data']['last_reset'] = datetime.strptime(data['nutrition_data']['last_reset'], '%Y-%m-%d').date()
        data['workout_data']['last_reset'] = datetime.strptime(data['workout_data']['last_reset'], '%Y-%m-%d').date()
        
        # Update session state
        st.session_state.hunter_data = data['hunter_data']
        st.session_state.nutrition_data = data['nutrition_data']
        st.session_state.workout_data = data['workout_data']
        st.session_state.achievements = data['achievements']
        
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

# Sidebar for data management and quick stats
def display_sidebar():
    st.sidebar.title("🎮 Hunter Control Panel")
    
    # Quick stats
    st.sidebar.metric("Hunter Level", st.session_state.hunter_data['level'])
    st.sidebar.metric("Total XP", f"{st.session_state.hunter_data['total_xp']:,}")
    st.sidebar.metric("Workouts Done", st.session_state.hunter_data['workouts_completed'])
    
    st.sidebar.divider()
    
    # Data management
    st.sidebar.subheader("💾 Data Management")
    
    # Export data
    data_json = save_data()
    st.sidebar.download_button(
        label="💾 Download Data File",
        data=data_json,
        file_name=f"hunter_data_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    # Import data
    uploaded_file = st.sidebar.file_uploader("📥 Import Hunter Data", type=['json'])
    if uploaded_file is not None:
        try:
            json_data = uploaded_file.read().decode('utf-8')
            if load_data(json_data):
                st.sidebar.success("✅ Data imported successfully!")
                st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Error importing data: {e}")
    
    st.sidebar.divider()
    
    # Quick actions
    st.sidebar.subheader("⚡ Quick Actions")
    
    if st.sidebar.button("🎯 Mark Day as Active"):
        if st.session_state.hunter_data['last_active'] != datetime.now().strftime('%Y-%m-%d'):
            st.session_state.hunter_data['days_active'] += 1
            st.session_state.hunter_data['streak'] += 1
            st.session_state.hunter_data['last_active'] = datetime.now().strftime('%Y-%m-%d')
            add_xp(25)
            st.sidebar.success("✅ Day marked as active! +25 XP")
        else:
            st.sidebar.warning("Already marked active today!")
    
    with st.sidebar.expander("🔄 Reset Weekly Progress"):
        if st.button("Confirm Reset", type="primary"):
            for day in st.session_state.workout_data:
                if day != 'last_reset':
                    st.session_state.workout_data[day] = {'completed': False, 'exercises': []}
            st.success("Weekly progress reset!")
            st.rerun()
    
    st.sidebar.divider()
    
    # Hunter tips
    st.sidebar.subheader("💡 Hunter Tips")
    tips = [
        "🥩 Hit protein target first - it preserves muscle!",
        "💧 Drink 3-4L water daily for optimal recovery",
        "😴 7-9 hours sleep = maximum XP gains",
        "🔥 Consistency beats perfection every time",
        "⏰ Time carbs around workouts for energy",
        "📸 Take progress photos weekly",
        "🎯 Small daily wins = massive results"
    ]
    
    daily_tip = random.choice(tips)
    st.sidebar.info(daily_tip)

# Enhanced nutrition suggestions
def display_meal_suggestions():
    st.subheader("🍽️ Hunter Meal Suggestions")
    
    # Calculate remaining macros
    remaining_cals = max(0, 1790 - st.session_state.nutrition_data['daily_calories'])
    
    if remaining_cals > 100:  # Only show if significant calories remain
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🥩 High Protein Options**")
            protein_foods = [
                {"name": "Grilled Chicken (200g)", "cal": 330, "pro": 62, "car": 0, "fat": 7},
                {"name": "Greek Yogurt (200g)", "cal": 130, "pro": 20, "car": 9, "fat": 0},
                {"name": "Egg Whites (4 large)", "cal": 68, "pro": 14, "car": 1, "fat": 0},
                {"name": "Tuna Can (185g)", "cal": 185, "pro": 40, "car": 0, "fat": 1},
                {"name": "Whey Protein (30g)", "cal": 120, "pro": 25, "car": 2, "fat": 1}
            ]
            
            for food in protein_foods:
                if st.button(f"Add {food['name']}", key=f"protein_{food['name']}"):
                    log_food(food)
                    st.rerun()
        
        with col2:
            st.write("**🍞 Quality Carbs**")
            carb_foods = [
                {"name": "Brown Rice (150g cooked)", "cal": 216, "pro": 5, "car": 45, "fat": 2},
                {"name": "Sweet Potato (200g)", "cal": 180, "pro": 4, "car": 41, "fat": 0},
                {"name": "Oatmeal (80g dry)", "cal": 304, "pro": 11, "car": 54, "fat": 6},
                {"name": "Banana (120g)", "cal": 107, "pro": 1, "car": 27, "fat": 0},
                {"name": "Quinoa (150g cooked)", "cal": 172, "pro": 6, "car": 31, "fat": 3}
            ]
            
            for food in carb_foods:
                if st.button(f"Add {food['name']}", key=f"carbs_{food['name']}"):
                    log_food(food)
                    st.rerun()
        
        with col3:
            st.write("**🥑 Healthy Fats**")
            fat_foods = [
                {"name": "Avocado (100g)", "cal": 160, "pro": 2, "car": 9, "fat": 15},
                {"name": "Almonds (30g)", "cal": 174, "pro": 6, "car": 6, "fat": 15},
                {"name": "Olive Oil (1 tbsp)", "cal": 119, "pro": 0, "car": 0, "fat": 14},
                {"name": "Salmon (150g)", "cal": 231, "pro": 31, "car": 0, "fat": 11},
                {"name": "Peanut Butter (20g)", "cal": 118, "pro": 5, "car": 4, "fat": 10}
            ]
            
            for food in fat_foods:
                if st.button(f"Add {food['name']}", key=f"fats_{food['name']}"):
                    log_food(food)
                    st.rerun()
    
    remaining_protein = max(0, 157 - st.session_state.nutrition_data['daily_protein'])
    remaining_carbs = max(0, 179 - st.session_state.nutrition_data['daily_carbs'])
    remaining_fats = max(0, 50 - st.session_state.nutrition_data['daily_fats'])
    
    st.info(f"""
    **🎯 Remaining Daily Targets:**
    - Calories: {remaining_cals:.0f}
    - Protein: {remaining_protein:.1f}g
    - Carbs: {remaining_carbs:.1f}g  
    - Fats: {remaining_fats:.1f}g
    """)

# Utility function for logging food from suggestions
def log_food(food):
    st.session_state.nutrition_data['daily_calories'] += food['cal']
    st.session_state.nutrition_data['daily_protein'] += food['pro']
    st.session_state.nutrition_data['daily_carbs'] += food['car']
    st.session_state.nutrition_data['daily_fats'] += food['fat']
    
    food_entry = {
        'name': food['name'],
        'calories': food['cal'],
        'protein': food['pro'],
        'carbs': food['car'],
        'fats': food['fat'],
        'time': datetime.now().strftime('%H:%M')
    }
    st.session_state.nutrition_data['food_log'].append(food_entry)
    add_xp(10)

# Main execution block
if __name__ == "__main__":
    main()