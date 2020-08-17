"""SQLAlchemy models and utility functions for this app"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '[User {}]'.format(self.name)


class Tweet(DB.Model):
    """Tweets and their embeddings from Basilica"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


class Visit(DB.Model):
    """Count number of visitors to this app"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    num_visits = DB.Column(DB.BigInteger)

    def __init__(self):
        self.num_visits = 1

