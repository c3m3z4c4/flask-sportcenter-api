from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mezadigi_dbtest2:4nonimouS@mx46.hostgator.mx:3306/mezadigi_sportcenter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


app.secret_key = 'mysecretkey'
###Models####


class Article(db.Model):
    __tablename__ = "articles"
    sku = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(70))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    def __init__(self, article, description, price, stock):
        self.article = article
        self.description = description
        self.price = price
        self.stock = stock


db.create_all()

# Schemas


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('sku', 'article', 'description', 'price', 'stock')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/articles', methods=['Post'])
def create_article():
    article = request.json['article']
    description = request.json['description']
    price = request.json['price']
    stock = request.json['stock']

    new_article = Article(article, description, price, stock)

    db.session.add(new_article)
    db.session.commit()

    return article_schema.jsonify(new_article)


@app.route('/articles', methods=['GET'])
def get_articles():
    all_articles = Article.query.all()
    result = articles_schema.dump(all_articles)
    return jsonify(result)


@app.route('/articles/<sku>', methods=['GET'])
def get_task(sku):
    article = Article.query.get(sku)
    return article_schema.jsonify(article)


@app.route('/article/<id>', methods=['PUT'])
def update_article(sku):
    article = Article.query.get(sku)

    article = request.json['article']
    description = request.json['description']
    price = request.json['price']
    stock = request.json['stock']

    article.article = article
    article.description = description
    article.price = price
    article.stock = stock

    db.session.commit()

    return article_schema.jsonify(article)


@app.route('/articles/<sku>', methods=['DELETE'])
def delete_article(sku):
    article = Article.query.get(sku)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({'message': 'Sport Center API... Wellcome'})


if __name__ == "__main__":
    app.run(debug=True)
