"""Main app/routing file for TwitOff."""

from os import getenv
from flask import Flask, render_template, request, jsonify
from .models import DB, User, Visit
from .predict import predict_user
from .twitter import add_or_update_user, add_users, update_all_users
# insert_test_users
import random


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')  # 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    DB.init_app(app)

    @app.route('/')
    def root():
        # A route can return a string or a template (which returns a string)
        visits = Visit.query.one()
        visits.num_visits += 1
        DB.session.commit()
        return render_template('base.html', title='Home', users=User.query.all(),
                               counter=visits.num_visits)

    def increment_visit():
        visits = Visit.query.one()
        visits.num_visits += 1
        DB.session.commit()
        return visits.num_visits

    @app.route('/random')
    def index():
        return render_template('random.html', title='Random number',
                               message=arbitrary_func())
        # return jsonify(arbitrary_func())

    def arbitrary_func():
        rand_num = random.randint(0, 100)
        return f'The random number for today is {rand_num}'

    @app.route('/add_test_users')
    def add_users():
        DB.drop_all()
        DB.create_all()
        # add_test_users()
        return 'Users added!'

    @app.route('/view_test_users')
    def view_users():
        users = User.query.all()
        return '\n'.join([str(user) for user in users])

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name'] # Dictionary of users
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'], # sorted alphabetically no matter what
                               request.values['user2']])
        if user1 == user2:
            message = 'Logic error. We stipulate the property of identity. See: Aristotle.'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])  # Gets back array([0.]) or [1.]
            message = '{} is more likely to tweet "{}" than {}'.format(
                user1 if prediction else user2,
                request.values['tweet_text'],
                user2 if prediction else user1
            )
        return render_template('prediction.html', title='Prediction',
                               message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()  # Reset the DB
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', users=User.query.all(),
                               title='All users and tweets updated!')

    return app
