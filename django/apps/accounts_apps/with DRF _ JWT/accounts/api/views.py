from .serializers import AddUserSerializer

from rest_framework.generics import CreateAPIView

class SignUpAPIView(CreateAPIView):
    serializer_class = AddUserSerializer