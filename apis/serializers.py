from rest_framework import serializers
from reports.models import CustomUser, LeakReport

class LeakReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = LeakReport
    fields = '__all__'
    read_only_fields = ['reporter', 'created_at']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'email', 'user_type']
