from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseGetUserDtoSchema(Schema):
    login = fields.Integer(required=True, allow_none=False)


class ResponseGetUserDto(ResponseDto, ResponseGetUserDtoSchema):
    __schema__ = ResponseGetUserDtoSchema
