from django.contrib import admin
from .models import Administrator, Booking, Client, Lawyer, Feedback

# Register your models here.
class administratorAdmin(admin.ModelAdmin):
    list_display = ('administrator_id', 'first_name', 'last_name', 'email', 'password', 'status', 'address')

class bookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'date', 'description', 'client_id', 'lawyer_id', 'status', 'user_first_name', 'user_last_name', 'lawyer_first_name', 'lawyer_last_name')

class clientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'first_name', 'last_name', 'email', 'password', 'status', 'role', 'contact_number', 'full_address', 'city', 'zip_code', 'image')
    
class lawyerAdmin(admin.ModelAdmin):
    list_display = ('lawyer_id', 'first_name', 'last_name', 'email', 'password', 'status', 'role', 'contact_number', 'university_college', 'degree', 'passing_year', 'full_address', 'city', 'zip_code', 'practise_length', 'case_handle', 'speciality', 'image')
    
class feedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'feedback')
    
# class userAdmin(admin.ModelAdmin):
#     list_display = ('u_id', 'first_name', 'last_name', 'email', 'password', 'status', 'role')

admin.site.register(Administrator, administratorAdmin)
admin.site.register(Booking, bookingAdmin)
admin.site.register(Client, clientAdmin)
admin.site.register(Lawyer, lawyerAdmin)
admin.site.register(Feedback, feedbackAdmin)
# admin.site.register(User, userAdmin)
