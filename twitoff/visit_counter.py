from flask import Flask # , jsonify
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# DB = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB.init_app(app)
#
#
# class Visit(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     count = db.Column(db.Integer)
#
#     def __init__(self):
#         self.count = 0


@app.route('/')
def counter():
    return 'Hello, world'
#     v = Visit.query.first()
#     if not v:
#         v = Visit()
#         v.count += 1
#         DB.session.add(v)
#     v.count += 1
#     DB.session.commit()
#     return jsonify(counter=v.count)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
