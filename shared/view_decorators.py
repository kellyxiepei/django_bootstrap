import functools
import json

from shared.response import GenericJsonResponse


def json_request(request_schema_class=None):
    def deco(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if request_schema_class is None:
                request.json = json.loads(request.body.decode(encoding='utf-8'))
            else:
                schema = request_schema_class()
                try:
                    request.data = schema.load(json.loads(request.body.decode(encoding='utf-8')))
                except Exception as e:
                    return GenericJsonResponse(code=1, message=str(e), data={})

            return func(request, *args, **kwargs)

        return wrapper

    return deco
