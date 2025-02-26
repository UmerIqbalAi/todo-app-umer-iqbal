import streamlit as st # type: ignore
import time
import datetime

# Initialize session state for tasks and points if not already done
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []
if 'points' not in st.session_state:
    st.session_state['points'] = 0
if 'completed_tasks' not in st.session_state:
    st.session_state['completed_tasks'] = []

# App title
st.title("⏳ Time-Tracked To-Do List with Rewards")

# Add new task
st.header("Add a New Task")
task_name = st.text_input("Task Name:")
task_duration = st.number_input("Duration (hours):", min_value=0.5, max_value=24.0, step=0.5)

task_deadline = st.time_input("Deadline:", datetime.time(23, 59))

if st.button("Add Task"):
    if task_name:
        st.session_state['tasks'].append({
            "name": task_name,
            "duration": task_duration,
            "deadline": task_deadline,
            "completed": False
        })
        st.success(f"Task '{task_name}' added successfully!")

# Display tasks
st.header("Your Tasks")
for index, task in enumerate(st.session_state['tasks']):
    col1, col2, col3 = st.columns([4, 2, 2])
    col1.text(f"{task['name']} - {task['duration']} hrs by {task['deadline']}")
    if not task['completed']:
        if col2.button(f"✅ Complete", key=f"complete_{index}"):
            task['completed'] = True
            st.session_state['completed_tasks'].append(task['name'])
            points_earned = 5 if task['duration'] <= 2 else 10
            st.session_state['points'] += points_earned
            st.success(f"Congrats! You've earned {points_earned} points. Your score: {st.session_state['points']}")
        if col3.button(f"❌ Not Done", key=f"not_done_{index}"):
            st.session_state['points'] -= 5
            st.error(f"Task not completed. You lost 5 points. Your score: {st.session_state['points']}")
    else:
        col1.text("✅ Completed")

# Display points and reward system
st.header("🎁 Your Reward Points: ")
st.metric(label="Points", value=st.session_state['points'])

st.subheader("Rewards System")
if st.session_state['points'] >= 20:
    st.success("🍿 Movie Night unlocked!")
if st.session_state['points'] >= 50:
    st.success("🚴 Cycling Trip unlocked!")
if st.session_state['points'] >= 75:
    st.success("🎉 Biryani Party unlocked!")
if st.session_state['points'] >= 100:
    st.success("🚗 New Car unlocked! (Just for fun)")
else:
    st.info("Keep completing tasks to earn rewards!")

# Reset tasks
if st.button("Reset All Tasks"):
    st.session_state['tasks'] = []
    st.session_state['completed_tasks'] = []
    st.session_state['points'] = 0
    st.warning("Tasks and points have been reset!")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | By Umer Iqbal")
