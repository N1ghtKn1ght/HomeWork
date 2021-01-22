import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseGetMessagesDtoSchema(Schema):
    id = fields.Int(required=True)
    sender = fields.Str(required=True)
    message = fields.Str(required=True)




class ResponseGetMessagesDto(ResponseDto):
    __schema__ = ResponseGetMessagesDtoSchema


