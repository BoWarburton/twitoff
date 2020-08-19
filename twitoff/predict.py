"""Prediction which user most similar to arbitrary tweet text"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA


def predict_user(user1_name, user2_name, tweet_text):
    """Get user objects, make embeddings for their tweets as X,
    who tweeted as y, fit model, return prediction"""
    """e.g. predict_user('BoWarburton', 'AlexBerenson', 'SARS-CoV-2') should return AlexBerenson"""
    user1 = User.query.filter(User.name == user1_name).one()  # It would be good to error check
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])  # X - vstack same columns, takes list
    labels = np.concatenate([np.ones(len(user1.tweets)),  # y - join arrays along existing axis
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
