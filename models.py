# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class AllenStreetTable(db.Model):
    __tablename__ = 'allenstreettable'
    __table_args__ = {'schema': 'public'}

    source_document = db.Column("source document", db.Text)
    # Define a composite primary key to uniquely identify each row.
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
