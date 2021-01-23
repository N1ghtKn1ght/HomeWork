import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponsePatchMessageDtoSchema(Schema):
    id = fields.Int()
    updated_at = fields.DateTime()
    message = fields.Str()

    @pre_load
    @post_load
    def deserialize_datetime(self, data: dict, **kwargs) -> dict:
        if 'updated_at' in data:
            data['updated_at'] = self.datetime_to_iso(data['updated_at'])
        return data

    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt, datetime.datetime):
            return dt.isoformat()
        return dt


class ResponsePatchMessageDto(ResponseDto, ResponsePatchMessageDtoSchema):
    __schema__ = ResponsePatchMessageDtoSchema
