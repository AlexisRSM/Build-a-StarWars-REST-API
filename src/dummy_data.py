import os
from faker import Faker
from models import db, User, Character, Planet, Favourite
from werkzeug.security import generate_password_hash
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
fake = Faker()

def create_fake_users(n):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=generate_password_hash(fake.password())
        )
        db.session.add(user)
    db.session.commit()

def create_fake_planets(n):
    for _ in range(n):
        planet = Planet(
            name=fake.name(),
            climate=fake.word(),
            terrain=fake.word()
        )
        db.session.add(planet)
    db.session.commit()

def create_fake_characters(n):
    planet_ids = [planet.id for planet in Planet.query.all()]
    for _ in range(n):
        character = Character(
            name=fake.name(),
            description=fake.text(),
            planet_id=fake.random_element(planet_ids)
        )
        db.session.add(character)
    db.session.commit()

def create_fake_favourites(n):
    user_ids = [user.id for user in User.query.all()]
    character_ids = [character.id for character in Character.query.all()]
    planet_ids = [planet.id for planet in Planet.query.all()]

    for _ in range(n):
        favourite = Favourite(
            user_id=fake.random_element(user_ids),
            character_id=fake.random_element(character_ids) if fake.boolean() else None,
            planet_id=fake.random_element(planet_ids) if fake.boolean() else None
        )
        db.session.add(favourite)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        # Create the database and the database tables
        db.create_all()

        # Add fake data
        create_fake_users(10)
        create_fake_planets(5)
        create_fake_characters(15)
        create_fake_favourites(20)

        print("Dummy data inserted successfully")
