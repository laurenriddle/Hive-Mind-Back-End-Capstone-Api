"""hivemind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from hivemindapi.models import *
from hivemindapi.views import Applicants, Users, Interviews, Industries, Companies, Cohorts, register_user, login_user, Favorites, Friends
router = routers.DefaultRouter(trailing_slash=False)

# This is just a generic route
# router.register(r'plural', ViewName, 'singular')
router.register(r'users', Users, 'user')
router.register(r'applicants', Applicants, 'applicant')
router.register(r'interviews', Interviews, 'interview')
router.register(r'industries', Industries, 'industry')
router.register(r'companies', Companies, 'company')
router.register(r'cohorts', Cohorts, 'cohort')
router.register(r'favorites', Favorites, 'favorite')
router.register(r'friends', Friends, 'friend')




urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]