from django.db import models
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class SurveyResponse(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    favorite_color = models.CharField(max_length=50)
    favorite_fruit = models.CharField(max_length=50)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class datatab(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    favorite_color = models.CharField(max_length=50)
    favorite_fruit = models.CharField(max_length=50)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"