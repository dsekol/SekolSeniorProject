# routes.py
from flask import Blueprint, request, jsonify, render_template
import time
from gpt import generate_text
from models import db, ChatbotResponses, AllenStreetTable

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    print("Thinking...")
    time.sleep(2)

    ai_reply = generate_text(user_message)
    chat_entry = ChatbotResponses(user_input=user_message, reply=ai_reply)
    try:
        db.session.add(chat_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error saving chat history:", e)

    return jsonify({"reply": ai_reply})

@bp.route("/chat_history", methods=["GET"])
def chat_history():
    chats = ChatbotResponses.query.order_by(ChatbotResponses.id.desc()).all()
    return jsonify([chat.as_dict() for chat in chats])

@bp.route("/allenstreetdata", methods=["GET"])
def allenstreet_data():
    rows = AllenStreetTable.query.all()
    return jsonify([row.as_dict() for row in rows])
