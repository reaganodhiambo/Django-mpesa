from django.contrib.auth.models import User
from django.http import HttpResponse

from .serializers import LNMOnlineSerializer
from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import AllowAny
from ..models import LNMOnline


class LNMOnlineAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self,request):
        print(request.data, "this is request.data")
        return HttpResponse (request.data, "this is request.data")