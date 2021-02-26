from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mezadigi_dbtest2:4nonimouS@mx46.hostgator.mx:3306/mezadigi_sportcenter'
db = SQLAlchemy(app)

app.secret_key = 'mysecretkey'
###Models####


class Article(db.Model):
    __tablename__ = "articles"
    sku = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, sku, article, description, price, stock):
        self.sku = sku
        self.article = article
        self.description = description
        self.price = price
        self.stock = stock

    def __repr__(self):
        return '' % self.sku


db.create_all()


class ArticleSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Article
        sqla_session = db.session
    sku = fields.Number(dump_only=True)
    article = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Number(required=True)
    stock = fields.Number(required=True)


@app.route('/articles', methods=['GET'])
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
    db.session.commit()
    return make_response("", 204)


@app.route('/add', methods=['POST'])
def create_article(payload):
    data = request.get_json(payload)
    article_schema = ArticleSchema()
    article = article_schema.load(data)
    result = article_schema.dump(article.create())
    return make_response(jsonify({result}), 200)


if __name__ == "__main__":
    app.run(debug=True)
