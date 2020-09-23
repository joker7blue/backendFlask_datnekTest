from app import db

class Language(db.Model):

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10))
    level_speak = db.Column(db.Integer)
    level_write = db.Column(db.Integer)
    level_comprehension = db.Column(db.Integer)