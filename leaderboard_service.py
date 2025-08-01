import json
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"

def update_leaderboard(session):
    entry = {
        "name": session['name'],
        "email": session['email'],
        "score": session['score'],
        "date": str(datetime.now()),
        "feedback": session.get('feedback', {})
    }
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            board = json.load(f)
    else:
        board = []
    board.append(entry)
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=2)
