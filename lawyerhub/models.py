from django.db import models

# Create your models here.
class Administrator(models.Model):
    administrator_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(default=None)
    password = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=255, default=None)
    address = models.TextField()
    
class Booking(models.Model):
    booking_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    date = models.DateField()
    description = models.TextField()
    client_id = models.CharField(max_length=255)
    lawyer_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    user_first_name = models.CharField(max_length=255, default=None)
    user_last_name = models.CharField(max_length=255, default=None)
    lawyer_first_name = models.CharField(max_length=255, default=None)
    lawyer_last_name = models.CharField(max_length=255, default=None)
    
class Client(models.Model):
    client_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(default=None)
    password = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=255, default=None)
    role = models.CharField(max_length=255, default=None)
    contact_number = models.CharField(max_length=15)
    full_address = models.TextField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    image = models.ImageField()
    
class Lawyer(models.Model):
    lawyer_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(default=None)
    password = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=255, default=None)
    role = models.CharField(max_length=255, default=None)
    contact_number = models.CharField(max_length=15)
    university_college = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    passing_year = models.CharField(max_length=100)
    full_address = models.TextField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    practise_length = models.CharField(max_length=255)
    case_handle = models.TextField()
    speciality = models.CharField(max_length=255)
    image = models.ImageField()
    
class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()
    
# class User(models.Model):
#     u_id = models.CharField(max_length=255)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     password = models.CharField(max_length=255)
#     status = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
