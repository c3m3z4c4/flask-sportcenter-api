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
<<<<<<< HEAD
    sku = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(70))
    description = db.Column(db.String(100))
=======
    sku = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article = db.Column(db.String(255))
    description = db.Column(db.String(255))
>>>>>>> 605612493c63765d1ed1fae4416cd30225753edc
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
<<<<<<< HEAD
def get_articles():
    all_articles = Article.query.all()
    result = article_schema.dump(all_articles)
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
=======
def index():
    get_articles = Article.query.all()
    article_schema = ArticleSchema(many=True)
    articles = article_schema.dump(get_articles)
    return make_response(jsonify(articles))


@app.route('/edit/<sku>', methods=['GET'])
def get_article_by_sku(sku):
    get_article = Article.query.get(sku)
    article_schema = ArticleSchema()
    article = article_schema.dump(get_article)
    return make_response(jsonify(article))


@app.route('/update/<sku>', methods=['PUT'])
def update_article_by_sku(sku):
    data = request.get_json()
    get_article = Article.query.get(sku)
    if data.get('article'):
        get_article.article = data['article']
    if data.get('description'):
        get_article.description = data['description']
    if data.get('price'):
        get_article.price = data['price']
    if data.get('stock'):
        get_article.stock = data['stock']
    db.session.add(get_article)
    db.session.commit()
    article_schema = ArticleSchema(
        only=['sku', 'article', 'description', 'price', 'stock'])
    article = article_schema.dump(get_article)
    return make_response(jsonify({article}))


@app.route('/delete/<sku>', methods=['DELETE'])
def delete_article_by_sku(sku):
    get_article = Article.query.get(sku)
    db.session.delete(get_article)
>>>>>>> 605612493c63765d1ed1fae4416cd30225753edc
    db.session.commit()
    return article_schema.jsonify(article)


<<<<<<< HEAD
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Sport Center API... Wellcome'})
=======
@app.route('/add', methods=['POST'])
def create_article():
    data = request.get_json()
    article_schema = ArticleSchema()
    article = article_schema.load(data)
    result = article_schema.dump(article.create())
    return make_response(jsonify({result}), 200)
>>>>>>> 605612493c63765d1ed1fae4416cd30225753edc


if __name__ == "__main__":
    app.run(debug=True)
