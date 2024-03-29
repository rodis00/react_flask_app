from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# classes
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body


# serialization object
class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


# app views
@app.route('/get', methods=['GET'])
def get_articles():
    articles = Articles.query.all()
    results = articles_schema.dump(articles)

    return jsonify(results)


@app.route('/get/<int:id>', methods=['GET'])
def article_detail(id):
    article = Articles.query.get(id)
    if article is not None:
        return article_schema.jsonify(article)
    return {
        'Status': f'article with id:{id} not found'
    }


@app.route('/add', methods=['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()

    return article_schema.jsonify(articles)


@app.route('/update/<int:id>', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    if article is not None:
        title = request.json['title']
        body = request.json['body']

        article.title = title
        article.body = body
        db.session.commit()

        return article_schema.jsonify(article)
    return {
        'Status': f'article with id:{id} not found'
    }


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    if article is not None:
        db.session.delete(article)
        db.session.commit()

        return {
            'Status': f'article with id:{id} deleted successfully'
        }
    return {
        'Status': f'article with id:{id} not found'
    }


if __name__ == '__main__':
    # creating database command
    with app.app_context():
        db.create_all()
    app.run(debug=True)
