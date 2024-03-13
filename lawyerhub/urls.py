from django.urls import path
from . import views

app_name = 'lawyerhub'

urlpatterns = [
    path('', views.index, name='index'),
    path('lawyers', views.lawyers, name='lawyers'),
    path('about_us', views.about_us, name='about_us'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('search_lawyer', views.search_lawyer, name='search_lawyer'),
    path('single_lawyer/<str:l_id>', views.single_lawyer, name='single_lawyer'),
    path('lawyer_register', views.lawyer_register, name='lawyer_register'),
    path('user_register', views.user_register, name='user_register'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('lawyer_profile', views.lawyer_profile, name='lawyer_profile'),
    path('lawyer_edit_profile', views.lawyer_edit_profile, name='lawyer_edit_profile'),
    path('lawyer_booking', views.lawyer_booking, name='lawyer_booking'),
    path('accept_request/<int:booking_id>', views.accept_request, name='accept_request'),
    path('update_password_lawyer', views.update_password_lawyer, name='update_password_lawyer'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_edit_profile', views.user_edit_profile, name='user_edit_profile'),
    path('user_booking', views.user_booking, name='user_booking'),
    path('update_password_user', views.update_password_user, name='update_password_user'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_user', views.admin_user, name='admin_user'),
    path('block_user/<str:c_id>', views.block_user, name='block_user'),
    path('unblock_user/<str:c_id>', views.unblock_user, name='unblock_user'),
    path('admin_lawyer', views.admin_lawyer, name='admin_lawyer'),
    path('approve_lawyer/<str:law_id>', views.approve_lawyer, name='approve_lawyer'),
    path('feedbacks', views.feedbacks, name='feedbacks'),
]
