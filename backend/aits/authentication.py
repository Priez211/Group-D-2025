import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            # Get the token from the Authorization header
            token = auth_header.split(' ')[1]
            
            # Decode the token
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Get user from payload
            user = User.objects.get(username=payload['user_id'])
            
            # Ensure user role matches the token
            if user.role != payload['role']:
                raise AuthenticationFailed('Invalid authentication token')
                
            return (user, None)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('No user found for token')
        except (IndexError, KeyError):
            raise AuthenticationFailed('Invalid token format')