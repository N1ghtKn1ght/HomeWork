from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponsePatchUserDtoSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    id = fields.Int()
    login = fields.Str()
    update_at = fields.DateTime()


class ResponsePatchUserDto(ResponseDto, ResponsePatchUserDtoSchema):
    __schema__ = ResponsePatchUserDtoSchema
