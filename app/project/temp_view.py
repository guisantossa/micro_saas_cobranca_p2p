from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import CustomTokenCreateSerializer


class TestTokenView(APIView):
    def post(self, request):
        serializer = CustomTokenCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            print("Serializer validado, criando token...")
            token_data = serializer.create(serializer.validated_data)
            print(f"Token criado: {token_data}")
            return Response(token_data)
        else:
            print("Erros:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
