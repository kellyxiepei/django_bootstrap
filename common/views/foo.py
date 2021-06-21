from django.views import View

from common.api_schema import FooSchema, CreateFooSchema
from common.models import Foo
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request


class GetFoo(View):
    @staticmethod
    def get(request, pk):
        foo = Foo.objects.get(id=pk)
        return GenericJsonResponse(data=FooSchema().dump(foo))


class CreateFoo(View):
    @staticmethod
    @json_request(request_schema_class=CreateFooSchema)
    def post(request):
        foo = Foo(**request.data)
        foo.save()
        return GenericJsonResponse(data=FooSchema().dump(foo))
