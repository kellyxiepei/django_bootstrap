from django.http import JsonResponse


class GenericJsonResponse(JsonResponse):
    def __init__(self, data, code=0, message='ok'):
        super(GenericJsonResponse, self).__init__(data={
            'code': code,
            'message': message,
            'data': data
        })
