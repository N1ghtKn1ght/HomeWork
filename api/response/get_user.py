from marshmallow import Schema, fields


class ResponseGetUserDtoSchema(Schema):
    login = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)



