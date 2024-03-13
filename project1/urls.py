"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Legal Services with LegalEase Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Legal Services with LegalEase Admin Panel"

urlpatterns = [
    path('', include('lawyerhub.urls')),
    path('lawyers/', include('lawyerhub.urls')),
    path('about_us/', include('lawyerhub.urls')),
    path('contact_us/', include('lawyerhub.urls')),
    path('search_lawyer/', include('lawyerhub.urls')),
    path('single_lawyer/', include('lawyerhub.urls')),
    path('lawyer_register/', include('lawyerhub.urls')),
    path('user_register/', include('lawyerhub.urls')),
    path('logout/', include('lawyerhub.urls')),
    path('login/', include('lawyerhub.urls')),
    path('lawyer_profile/', include('lawyerhub.urls')),
    path('lawyer_edit_profile/', include('lawyerhub.urls')),
    path('lawyer_booking/', include('lawyerhub.urls')),
    path('accept_request/', include('lawyerhub.urls')),
    path('update_password_lawyer/', include('lawyerhub.urls')),
    path('user_profile/', include('lawyerhub.urls')),
    path('user_edit_profile/', include('lawyerhub.urls')),
    path('user_booking/', include('lawyerhub.urls')),
    path('update_password_user/', include('lawyerhub.urls')),
    path('admin_dashboard/', include('lawyerhub.urls')),
    path('admin_user/', include('lawyerhub.urls')),
    path('block_user/', include('lawyerhub.urls')),
    path('unblock_user/', include('lawyerhub.urls')),
    path('admin_lawyer/', include('lawyerhub.urls')),
    path('approve_lawyer/', include('lawyerhub.urls')),
    path('feedbacks/', include('lawyerhub.urls')),
    path('admin/', admin.site.urls),
]
