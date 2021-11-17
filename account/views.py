from django.http.response import JsonResponse
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import authenticate, login


def get_csrf(request):
    response = JsonResponse({'info': 'Success - Set CSRF cookie'})
    response['X-CSRFToken'] = get_token(request)
    return response


@require_POST
def loginView(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return JsonResponse({'info': 'Username and passowrd is needed'})

    user = authenticate(username=email, password=password)

    if user is None:
        return JsonResponse({'info': 'User does not exist'}, status=400)

    login(request, user)
    return JsonResponse({'info': 'User logged in successfully'})
