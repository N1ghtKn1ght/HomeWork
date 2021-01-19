from marshmallow import Schema, fields


class ResponseGetMessagesDtoSchema(Schema):
    id = fields.Int(required=True)
    sender = fields.Str(required=True)
    message = fields.Str(required=True)



