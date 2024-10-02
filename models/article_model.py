from datetime import datetime
from flask import jsonify
from marshmallow import ValidationError
from error_handler import ErrorHandler
from request.article_request import ArticleSchema
import logging
from app import db


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    @staticmethod
    def delete(id):
        try:
            article = Article.query.get(id)
            db.session.delete(article)
            db.session.commit()
            return {'success': True, 'message': 'Article deleted successfully'}, 200
        except Exception as e:
            return ErrorHandler.handle_error(str(e))


    @staticmethod
    def index():
        return Article.query.order_by(Article.date.desc()).all()

    @staticmethod
    def show(id):
        return Article.query.get(id)


    @staticmethod
    def create(data):
        try:
            validated_data = Article.validation(data)

            article = Article(
                title=validated_data.get('title'),
                intro=validated_data.get('intro'),
                text=validated_data.get('text'),
                user_id=validated_data.get('user_id')
            )
            db.session.add(article)
            db.session.commit()

            return {'success': True, 'message': 'Article created successfully', 'article_id': article.id}, 201
        except ValidationError as err:
            return ErrorHandler.handle_validation_error(err.messages)
        except Exception as e:
            return ErrorHandler.handle_error(str(e))

    @staticmethod
    def update( data, id):
        try:
            article = Article.query.get(id)

            if not article:
                return {'success': False, 'message': 'Article not found'}, 404

            validated_data = Article.validation(data)
            article.title = validated_data.get('title')
            article.intro = validated_data.get('intro')
            article.text = validated_data.get('text')
            db.session.commit()

            return {'success': True, 'message': 'Article updated successfully', 'article_id': article.id}, 200
        except ValidationError as err:
            return ErrorHandler.handle_validation_error(err.messages)
        except Exception as e:
            return ErrorHandler.handle_error(str(e))



    @staticmethod
    def validation(data):
        schema = ArticleSchema()
        try:
            validated_data = schema.load(data)
            return validated_data  # Возвращаем валидированные данные, если ошибок нет
        except ValidationError as err:
            raise ValidationError(err.messages)  # Выбрасываем исключение для обработки ошибок выше


def __repr__(self):
        return '<Article %r>' % self.id