from django.urls import path

from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [

    # docs
    #path('docs/',include_docs_urls(title='Application API', public=False)),

    # URLS
    path('login/', views.LoginOrSignupAPI.as_view(), name='LoginAPI'),
]
