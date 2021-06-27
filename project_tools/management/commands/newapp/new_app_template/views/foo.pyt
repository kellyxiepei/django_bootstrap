from django.views import View

from ..api_schema import FooSchema, CreateFooSchema
from ..models import Foo
from shared.auth.demo.authenticator_demo import DemoAuthentication
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request, require_authentication


class GetFoo(View):
    def get(self, request, pk):
        foo = Foo.objects.get(id=pk)
        return GenericJsonResponse(data=FooSchema().dump(foo))


class CreateFoo(View):
    @require_authentication(authenticator_class=DemoAuthentication)
    @json_request(request_schema_class=CreateFooSchema)
    def post(self, request):
        foo = Foo(**request.data)
        foo.save()
        return GenericJsonResponse(data=FooSchema().dump(foo))
