
from marshmallow import Schema, fields, validate, ValidationError

class ArticleSchema(Schema):
    title = fields.Str(
        required=True,
        # validate=validate.Length(max=100),
        validate=[validate.Length(min=1, max=100)],
        error_messages={"required": "Title is required.", "validate": "Title cannot be longer than 100 characters."}
    )
    intro = fields.Str(
        required=True,
        validate=[validate.Length(min=1, max=300)],
        error_messages={"required": "Intro is required.", "validate": "Intro cannot be longer than 300 characters."}
    )
    text = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Text is required."}
    )
    user_id = fields.Int(missing=1)  # По умолчанию 1, если не передан

