from django.conf import settings
import jwt
from authentication.models import User
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            token = request.META.get('HTTP_AUTHORIZATION', False)
            if token:
                try:
                    payload = jwt.decode(token.split()[1], settings.SECRET_KEY)
                    request.user = User.objects.get(id=payload['user_id'])
                except:
                    pass
