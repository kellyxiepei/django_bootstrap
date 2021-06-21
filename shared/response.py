from django.http import JsonResponse


class GenericJsonResponse(JsonResponse):
    def __init__(self, code=0, message='成功', data=None):
        final_data = {
            'code': code,
            'message': message
        }
        if data is not None:
            final_data['data'] = data
        super(GenericJsonResponse, self).__init__(data=final_data)
