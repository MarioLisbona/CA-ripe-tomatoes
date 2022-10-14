from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow(app)

# ## DB CONNECTION AREA
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tomato:rotten123@127.0.0.1:5432/ripe_tomatoes_db'

db = SQLAlchemy(app)


# # SCHEMAS AREA

class ActorSchema(ma.Schema):
    class Meta:
        #fields to expose for actors
        fields = (
            'id',
            'first_name',
            'last_name',
            'gender',
            'country',
            'dob',
            'resides'
        )

class MovieSchema(ma.Schema):
    class Meta:
        #fields to expose for movies
        fields = (
            'id',
            'title',
            'genre',
            'length',
            'year_released',
            'rating'
        )

# #single schema for when single actor is returned
actor_schema = ActorSchema()

# #multiple schema for when multiple actors are returned
actors_schema = ActorSchema(many=True)

# #single schema for when single actor is returned
movie_schema = MovieSchema()

# #multiple schema for when multiple actors are returned
movies_schema = MovieSchema(many=True)



# # MODELS AREA
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    country = db.Column(db.String(100))
    dob = db.Column(db.Date)
    resides = db.Column(db.String(100))

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String(50))
    length = db.Column(db.Integer)
    year_released = db.Column(db.Date)
    rating = db.Column(db.String(5))



# # CLI COMMANDS AREA
@app.cli.command('create')
def create_db():
    db.create_all()
    print('\n=====================================================================')
    print('================== Database created successfully ! ==================')
    print('=====================================================================\n')


@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print('\n=====================================================================')
    print('================== Database deleted successfully ! ==================')
    print('=====================================================================\n')

@app.cli.command('seed')
def seed_db():
    movie1 = Movie(
        title = 'The Shawshank Redemption',
        genre = 'Drama',
        length = 160,
        year_released = date(1994, 4, 13),
        rating = 5
    )

    movie2 = Movie(
        title = 'Fight Club',
        genre = 'Drama',
        length = 120,
        year_released = date(1999, 6, 16),
        rating = 5
        )

    movie3 = Movie(
        title = 'Joker',
        genre = 'Drama',
        length = 140,
        year_released = date(2019, 6, 6),
        rating = 5
        )

    actor1 = Actor(
        first_name = 'William Bradley',
        last_name = 'Pitt',
        gender = 'Male',
        country = 'USA',
        dob =  date(1963, 12, 18),
        resides = 'Los Angeles, California'
    )

    actor2 = Actor(
        first_name = 'Chris',
        last_name = 'Hemsworth',
        gender = 'Male',
        country = 'Australia',
        dob =  date(1983, 8, 11),
        resides = 'Broken Head, Australia'
    )

    actor3 = Actor(
        first_name = 'Keanu',
        last_name = 'Reeves',
        gender = 'Male',
        country = 'USA',
        dob =  date(1964, 9, 2),
        resides = 'Honolulu, Hawaii'
    )

    actor4 = Actor(
        first_name = 'Adam',
        last_name = 'Sandler',
        gender = 'Male',
        country = 'USA',
        dob =  date(1966, 9, 9),
        resides = 'Los Angeles, California'
    )

    db.session.add(movie1, movie2, movie3)
    db.session.add(actor1, actor2, actor3, actor4)
    db.session.commit()
    print('\n====================================================================')
    print('================== Database seeded successfully ! ==================')
    print('====================================================================\n')

# ROUTING AREA

@app.route("/")
def hello():
    return "Welcome to Ripe Tomatoes API"

@app.route('/actors/', methods=['GET'])
def get_actors():
  #retrieve all the actors from the database table 'actors'
  actors_list = Actor.query.all()

  #Convert the actors from the database into a JSON format and store them in result
  result = actors_schema.dump(actors_list)

  #return the data in json format
  return jsonify(result)

@app.route('/movies/', methods=['GET'])
def get_movies():
  #retrieve all the actors from the database table 'actors'
  movies_list = Movie.query.all()

  #Convert the actors from the database into a JSON format and store them in result
  result = movies_schema.dump(movies_list)

  #return the data in json format
  return jsonify(result)