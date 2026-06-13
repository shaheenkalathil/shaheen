import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide"
)
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Oswald', sans-serif;
}

/* Main Background */
.stApp {
    background-color: #0F172A;
    color: #F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1E293B;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #06B6D4 !important;
}

/* Labels and Text */
label, p, span {
    color: #F8FAFC !important;
}

/* Main Title */
.main-title {
    text-align: center;
    color: #06B6D4 !important;
    font-size: 60px;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    background-color: #06B6D4;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #0891B2;
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #1E293B;
    color: white;
    border: 2px solid #06B6D4;
    border-radius: 10px;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1E293B;
    color: white;
}

/* Date Input */
.stDateInput {
    color: white;
}

/* Success Messages */
.stSuccess {
    background-color: #22C55E;
    color: white;
    border-radius: 8px;
}

/* Info Messages */
.stInfo {
    background-color: #1E293B;
    color: white;
    border-radius: 8px;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    background-color: #1E293B;
    border-radius: 10px;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #06B6D4;
    padding: 15px;
    border-radius: 12px;
}

/* Horizontal Line */
hr {
    border-color: #06B6D4;
}

</style>
""", unsafe_allow_html=True)

if "users" not in st.session_state:
    st.session_state.users = {}

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def register():

    st.header("Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if not username or not email or not password:
            st.error("Please fill all fields")

        elif username in st.session_state.users:
            st.error("Username already exists")

        else:

            st.session_state.users[username] = {
                "email": email,
                "password": password
            }

            st.session_state.tasks[username] = []

            st.success("Registration Successful!")

def login():

    st.header("Login")

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button("Login"):

        if (
            username in st.session_state.users
            and
            st.session_state.users[username]["password"] == password
        ):

            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()

        else:
            st.error("Invalid Username or Password")

def dashboard():

    user = st.session_state.current_user
    tasks = st.session_state.tasks[user]

    
    st.markdown(
        "<h1 class='main-title'>TASK MANAGER</h1>",
        unsafe_allow_html=True
    )

    st.success(f"Welcome {user}")

    # Dashboard Stats
    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📋 Total Tasks", total_tasks)

    with col2:
        st.metric("✅ Completed", completed_tasks)

    with col3:
        st.metric("⏳ Pending", pending_tasks)

    st.divider()

    # Create Task
    st.subheader("Create New Task")

    title = st.text_input("Task Title")

    description = st.text_area(
        "Task Description"
    )

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

    due_date = st.date_input(
        "Due Date",
        min_value=date.today()
    )

    if st.button("Add Task"):

        if title:

            task_id = len(tasks) + 1

            tasks.append(
                {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "due_date": str(due_date),
                    "completed": False
                }
            )

            st.success("Task Added Successfully")
            st.rerun()

        else:
            st.error("Task Title is required")

    st.divider()

    
    st.subheader("My Tasks")

    if tasks:

        df = pd.DataFrame(
            [
                {
                    "ID": task["id"],
                    "Task Title": task["title"],
                    "Description": task["description"],
                    "Priority":
                        "🟢 Low" if task["priority"] == "Low"
                        else "🟡 Medium" if task["priority"] == "Medium"
                        else "🔴 High",
                    "Due Date": task["due_date"],
                    "Completed":
                        "✅ Yes"
                        if task["completed"]
                        else "❌ No"
                }
                for task in tasks
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        st.subheader("Update Task Status")

        for index, task in enumerate(tasks):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.write(f"**{task['title']}**")

            with col2:

                if task["completed"]:
                    st.success("✅ Completed")

                else:
                    if st.button(
                        "Complete",
                        key=f"complete_{index}"
                    ):
                        task["completed"] = True
                        st.rerun()

            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{index}"
                ):
                    tasks.pop(index)
                    st.rerun()

    else:
        st.info("No Tasks Available")

    st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

if st.session_state.logged_in:

    dashboard()

else:

    st.markdown(
        "<h1 class='main-title'>TASK MANAGER</h1>",
        unsafe_allow_html=True
    )

    option = st.sidebar.selectbox(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )

    if option == "Login":
        login()
    else:
        register()