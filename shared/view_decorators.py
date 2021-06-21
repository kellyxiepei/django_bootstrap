import functools
import json

from marshmallow import ValidationError

from shared.response import GenericJsonResponse


def json_request(request_schema_class=None):
    def deco(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            request.json = json.loads(request.body.decode(encoding='utf-8'))
            if request_schema_class is not None:
                schema = request_schema_class()
                try:
                    request.data = schema.load(request.json)
                except ValidationError as e:
                    return GenericJsonResponse(code=1, message="请求参数不合法", data=e.messages)
            return func(request, *args, **kwargs)

        return wrapper

    return deco
