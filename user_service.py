import uuid
from datetime import datetime

def init_session(st):
    if "session" not in st.session_state:
        st.session_state.session = {
            "id": str(uuid.uuid4()),
            "name": "",
            "email": "",
            "data": [],
            "feedback": {},
            "score": 0,
            "completed": False,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
