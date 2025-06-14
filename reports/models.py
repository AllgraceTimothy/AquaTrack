from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .constants import STATUS_CHOICES, USER_TYPES, PRIORITY
from django.conf import settings

class CustomUser(AbstractUser):
  user_type = models.CharField(max_length=10, choices=USER_TYPES, default='public')

  def is_admin(self):
    return self.user_type == 'admin' or self.is_superuser
  
  def is_team(self):
    return self.user_type == 'team'
  
  def is_public(self):
    return self.user_type == 'public'

class LeakReport(models.Model):
  reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='leaks/')
  description = models.TextField(blank=True)
  latitude = models.FloatField()
  longitude = models.FloatField()
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
  priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
  created_at = models.DateTimeField(auto_now_add=True)
  assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')

  def __str__(self):
    return f"LeakedReport #{self.id} - {self.status}"
