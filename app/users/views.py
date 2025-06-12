from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from users.serializers import CustomTokenCreateSerializer


class CustomAuthTokenView(ObtainAuthToken):
    serializer_class = CustomTokenCreateSerializer

    def post(self, request, *args, **kwargs):
        print("🚀 CustomAuthTokenView disparada!")
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        print(f"✅ Token gerado para user_id={user.id}, cpf={user.cpf}")
        return Response({"auth_token": token.key})
