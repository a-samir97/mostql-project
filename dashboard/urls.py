from django.urls import path

from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [

    # docs
    path('docs/',include_docs_urls(title='My API title', public=False)),

    # URLS

    # Authentication (login, create user, logout)
    path('login/', views.LoginAPI.as_view(), name='LoginAPI'),
    path('signup/', views.CreateUser.as_view(), name='CreateUserAPI'),
    path('logout/', views.LogoutAPI.as_view(), name='LogoutAPI'),

    # logging users (saved data)
    path('logging/',views.LoggingAPI.as_view(), name='Logging'),

]
