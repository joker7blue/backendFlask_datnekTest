import os
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_cors import CORS
#from models.Language import Language


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

# SECRET KEY configuration for forms
app.config['SECRET_KEY'] = "@kalidoukAZkdkfdkfndnAdfdkoozvld"

# SQLALCHEMY configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# NB: THE APP CAN BE OPTIMIZE USING THE BLUEPRINT FEATURE, BUT THAT IS A SIMPLE APP

class Language(db.Model):

    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10))
    level_speak = db.Column(db.Integer)
    level_write = db.Column(db.Integer)
    level_comprehension = db.Column(db.Integer)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'level_speak': self.level_speak,
            'level_write': self.level_write,
            'level_comprehension': self.level_comprehension,
        }   
        return data


# Add Language
@app.route('/api/langs', methods=['POST'])
def add_lang():
    
    data = request.get_json()

    lang = Language(name=data['name'], code=data['code'], level_speak=data['level_speak'], level_write=data['level_write'], level_comprehension=data['level_comprehension'])
    db.session.add(lang)
    db.session.commit()

    return jsonify({'message': 'Lang add successfuly'})


# Get Languages
@app.route('/api/langs')
def get_langs():
    
    try:
        return jsonify({'data': [item.to_dict() for item in Language.query.order_by(Language.code.asc())]})
    except Exception as e:
        return jsonify({'error': e})


# Get Language
@app.route('/api/langs/<id>')
def get_one_langs(id):
    
    lang = Language.query.get_or_404(id)

    return jsonify({'data': lang.to_dict()})
    

# Update Language
@app.route('/api/langs/<id>', methods=['PUT'])
def update_langs(id):
    
    data = request.get_json()

    lang = Language.query.get_or_404(id)
    lang.name = data['name']
    lang.code = data['code']
    lang.level_speak = data['level_speak']
    lang.level_write = data['level_write']
    lang.level_comprehension = data['level_comprehension']

    db.session.add(lang)
    db.session.commit()

    return jsonify({'message': 'Success updated'})


# Delete Language
@app.route('/api/langs/<id>', methods=['DELETE'])
def delete_langs(id):
    
    lang = Language.query.get_or_404(id)
    db.session.delete(lang)
    db.session.commit()

    return jsonify({'message': 'Success deleted'})


if __name__ == "__main__":

    app.run(debug=True)