from django.contrib.auth.backends import ModelBackend
from users.models import User


class CPFBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        cpf = username or kwargs.get("cpf")
        print(f"\n🧠 Autenticando CPF={cpf}")
        if cpf is None or password is None:
            return None
        try:
            user = User.objects.get(cpf=cpf)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
