from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class RoleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        # Select Role page
        if request.path == "/select-role/":
            return self.get_response(request)

        # Select Role API
        if request.path == "/api/accounts/select-role/":
            return self.get_response(request)

        # Google authentication
        if (
            request.path.startswith("/accounts/google/")
            or
            request.path.startswith("/api/v1/auth/google/")
        ):
            return self.get_response(request)

        # API request
        if request.path.startswith("/api/"):

            try:

                result = self.jwt_auth.authenticate(request)
                if result:

                    user, token = result

                    if not user.role:
                        return JsonResponse({
                            "error": "ROLE_NOT_SET"
                        }, status=403)

                    if user.role == "provider":

                        print("Provider API request")

                    elif user.role in ["user", "admin"]:

                        print("User/Admin API request")

            except Exception as e:

                print("JWT ERROR:", e)

            return self.get_response(request)

        # Normal Django pages
        user = request.user

        if user.is_authenticated:

            print("SESSION USER:", user.id)
            print("SESSION ROLE:", user.role)

        return self.get_response(request)

 