from rest_framework import viewsets, permissions
from reports.models import LeakReport
from .serializers import LeakReportSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from reports.models import CustomUser as User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

class LeakReportViewSet(viewsets.ModelViewSet):
  queryset = LeakReport.objects.all().order_by('-created_at')
  serializer_class = LeakReportSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def app_signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
       return Response({'error': 'Username and password are required'}, status=400)
       
    if User.objects.filter(username=username).exists():
       return Response({'error': 'Username already taken'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def app_login(request):
    from django.contrib.auth import authenticate

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)
