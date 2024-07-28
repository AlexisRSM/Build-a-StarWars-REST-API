from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favourites = db.relationship('Favourite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship('Planet', back_populates='characters')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "planet_id": self.planet_id
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    characters = db.relationship('Character', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Favourite(db.Model):
    __tablename__ = 'favourite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character = db.relationship('Character', backref='favourites')
    planet = db.relationship('Planet', backref='favourites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }
