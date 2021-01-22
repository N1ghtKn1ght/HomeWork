from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseYourMessageDtoSchema(Schema):
    id = fields.Int(required=True)
    recipient = fields.Str(required=True)
    message = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)


class ResponseYourMessageDto(ResponseDto, ResponseYourMessageDtoSchema):
    __schema__ = ResponseYourMessageDtoSchema
