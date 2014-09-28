from django.contrib.auth import authenticate, login

__author__ = 'vladimirtsyupko'



class DefaultUserMiddleware(object):
    """
    Middleware that handles temporary messages.
    """

    def process_request(self, request):
        if not request.user.is_authenticated() and request.path not in ['/logout/', '/login/']:
            user = authenticate(
                username='guest@gmail.com',
                password='qwerty',
            )
            login(request, user)
            request.user = user
