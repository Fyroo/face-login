from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import importlib
from .models import User

def get_face_utils():
    """Lazy load face_utils module only when needed"""
    return importlib.import_module('.face_utils', package='accounts')

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        face_image_base64 = data.get('face_image')

        if not all([username, password, face_image_base64]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Process face image and get encoding
        face_utils = get_face_utils()
        face_encoding, error = face_utils.process_base64_image(face_image_base64)
        if error:
            return JsonResponse({'error': error}, status=400)

        # Create user with face encoding
        user = User.objects.create_user(username=username, password=password)
        user.set_face_encoding(face_encoding)
        user.save()

        return JsonResponse({'message': 'User registered successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_with_face(request):
    try:
        data = json.loads(request.body)
        face_image_base64 = data.get('face_image')

        if not face_image_base64:
            return JsonResponse({'error': 'Face image required'}, status=400)

        # Process face image and get encoding
        face_utils = get_face_utils()
        face_encoding, error = face_utils.process_base64_image(face_image_base64)
        if error:
            return JsonResponse({'error': error}, status=400)

        # Find matching user
        for user in User.objects.all():
            stored_encoding = user.get_face_encoding()
            if stored_encoding is not None:
                # Compare face encodings
                matches, error = face_utils.compare_face_encodings(stored_encoding, face_encoding)
                if matches:
                    login(request, user)
                    return JsonResponse({'message': 'Login successful', 'username': user.username})

        return JsonResponse({'error': 'No matching face found'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_with_credentials(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not all([username, password]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'username': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Successfully logged out'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
