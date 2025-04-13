from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import time  # For simulating chatbot "thinking"
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = Flask(__name__)
CORS(app)  # Enable frontend connection

# --- Configure PostgreSQL Database ---
# Connection string based on your provided DSN details:
# host=localhost, port=5432, dbname=postgres, user=postgres, password=Ninja@123,
# connect_timeout=10, sslmode=prefer.
# URL-encoded password: Ninja@123 → Ninja%40123.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:Ninja%40123@localhost:5432/postgres'
    '?connect_timeout=10&sslmode=prefer'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Define Database Models ---

# Model for the chatbot_responses table
class ChatbotResponses(db.Model):
    __tablename__ = 'chatbot_responses'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, unique=True)
    reply = db.Column(db.Text)

    def as_dict(self):
        return {
            'id': self.id,
            'user_input': self.user_input,
            'reply': self.reply
        }

# Model for the allenstreettable.
# Since this table does not have an explicit primary key, we define a composite primary key.
# Here we assume that the combination of "southern cross street of block",
# "northern cross street of block", and "house number" is unique.
class AllenStreetTable(db.Model):
    __tablename__ = 'allenstreettable'
    __table_args__ = {'schema': 'public'}

    source_document = db.Column("source document", db.Text)
    # Composite primary key columns:
    southern_cross = db.Column("southern cross street of block", db.Text, primary_key=True)
    northern_cross = db.Column("northern cross street of block", db.Text, primary_key=True)
    house_number = db.Column("house number", db.Text, primary_key=True)

    family_number = db.Column("family number (if residence)", db.Text)
    relationship_to_head = db.Column("relationship to head of household (if residence)", db.Text)
    surname = db.Column(db.Text)
    given_name = db.Column("given name", db.Text)
    birthplace = db.Column("birthplace (if resident)", db.Text)
    sex = db.Column(db.Text)
    year_born = db.Column("year born (if resident)", db.Text)
    age = db.Column("age (if resident)", db.Text)
    year_arrived = db.Column("year arrived (if resident; born in the usa if blank)", db.Text)
    years_in_usa = db.Column("years in usa (if resident)", db.Text)
    citizen_alien = db.Column("citizen/alien (if resident)", db.Text)
    occupation = db.Column(db.Text)
    business = db.Column("business (as listed in 1905 or 1906 trow's); h=home", db.Text)
    further_comments = db.Column("further comments", db.Text)

    def as_dict(self):
        return {
            'source_document': self.source_document,
            'southern_cross': self.southern_cross,
            'northern_cross': self.northern_cross,
            'house_number': self.house_number,
            'family_number': self.family_number,
            'relationship_to_head': self.relationship_to_head,
            'surname': self.surname,
            'given_name': self.given_name,
            'birthplace': self.birthplace,
            'sex': self.sex,
            'year_born': self.year_born,
            'age': self.age,
            'year_arrived': self.year_arrived,
            'years_in_usa': self.years_in_usa,
            'citizen_alien': self.citizen_alien,
            'occupation': self.occupation,
            'business': self.business,
            'further_comments': self.further_comments
        }

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# --- Load GPT-2 Model & Tokenizer from Saved Directory ---
MODEL_PATH = "./saved_model_gpt"  # Update this path to your model's directory
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH, local_files_only=True)

# 🔹 Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- Function to Generate AI-based Responses ---
def generate_text(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_return_sequences=1
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- Render Homepage with Chat Interface ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Flask API Endpoint for Chatbot Responses ---
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Get message from frontend

    print("Thinking...")  # Simulate a processing delay
    time.sleep(2)

    # Generate AI-based response
    ai_reply = generate_text(user_message)
    
    # Save conversation to the chatbot_responses table
    chat_entry = ChatbotResponses(user_input=user_message, reply=ai_reply)
    try:
        db.session.add(chat_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error saving chat history:", e)

    return jsonify({"reply": ai_reply})

# --- Endpoint to Retrieve Chat History ---
@app.route("/chat_history", methods=["GET"])
def chat_history():
    chats = ChatbotResponses.query.order_by(ChatbotResponses.id.desc()).all()
    return jsonify([chat.as_dict() for chat in chats])

# --- Endpoint to Retrieve AllenStreet Table Data ---
@app.route("/allenstreetdata", methods=["GET"])
def allenstreet_data():
    rows = AllenStreetTable.query.all()
    return jsonify([row.as_dict() for row in rows])

if __name__ == "__main__":
    app.run(debug=True)
