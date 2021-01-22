from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseGetUserDtoSchema(Schema):
    login = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class ResponseGetUserDto(ResponseDto):
    __schema__ = ResponseGetUserDtoSchema
