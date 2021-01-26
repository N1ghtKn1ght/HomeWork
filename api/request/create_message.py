from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    message = fields.Str(allow_none=False, required=True)
    recipient_id = fields.Int(allow_none=False, required=True)


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema
