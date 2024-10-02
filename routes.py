from flask import render_template, request, redirect, jsonify
from error_handler import ErrorHandler
from models import User, Article


def init_routes(app, db):

    @app.route('/')
    @app.route('/home')
    def index():
        return render_template("index.html")


    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/price')
    def price():
        return render_template("price.html")

    @app.route('/login')
    def login():
        return render_template("login.html")

    @app.route('/register')
    def register():
        return render_template("register.html")

    @app.route('/posts')
    def posts():
        articles=Article.index()
        return render_template("posts.html", articles=articles)


    @app.route('/posts/<int:id>')
    def post_detail(id):
        article = Article.show(id)
        return render_template("post_detail.html", article=article)



    @app.route('/posts/delete/<int:id>',methods=['DELETE'])
    def post_delete(id):
        response, status_code = Article.delete(id)
        return response, status_code


    @app.route('/posts/update/<int:id>', methods=['PUT', 'GET'])
    def post_update(id):
        article = Article.show(id)
        if request.method == 'PUT':
            data = request.get_json()
            response, status_code = Article.update(data, id)
            return response, status_code
        else:
            return render_template("post_update.html", article=article)


    @app.route('/create-article', methods=['POST'])
    def post_create():
            if request.is_json:
                data = request.get_json()
                response, status_code = Article.create(data)
                return response, status_code
            else:
                response = ErrorHandler.handle_validation_error('Request must be JSON')
                return jsonify(response), 400

