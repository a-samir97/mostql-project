from django.urls import path

from . import views

urlpatterns = [
    # URLS
    path('reg-login/', views.RegisteredLoginAPI.as_view(), name='LoginUserAPI'),
    path('unreg-login/', views.UnregisteredLoginAPI.as_view(), name='LoginUserAPI'),

    # Registered and Not Registered Users URLS
    path('registered-users/', views.ListRegisteredUserAPI.as_view(),name='RegisteredUserListAPI'),
    path('unregistered-users/', views.ListNotRegisteredUserAPI.as_view(),name='UnregisteredUserListAPI'),

    # Certified and Not Ceritifed Users URLS
    path('certified-users/', views.ListCertifiedUsersAPI.as_view(),name='CertifiedUserListAPI'),
    path('uncertified-users/', views.ListNotCertifiedUsersAPI.as_view(),name='UncertifiedUserListAPI'),

    # View Acccount API
    path('view/<str:name_id>/',views.ViewAccountAPI.as_view(), name='ViewAccountAPI'),

    # all Users URL
    path('all-users/', views.ListAllUserAPI.as_view(), name='AllUserListAPI'),

    # Search
    path('search-name/', views.SearchByNameID.as_view(), name='SearchByNameAPI'),
    path('search-bio/', views.SearchByBio.as_view(), name='SearchByBioAPI'),
    path('search-username/', views.SearchByUsername.as_view(), name='SeachByUsernameAPI'),
    path('search-nickname/', views.SearchByNickname.as_view(), name='SearchByNicknameAPI'),

    # Follow URL
    path('follow/<str:name_id>/', views.ToggleFollowingAPI.as_view(), name='FollowUserAPI'),

    # Add, confirm, reject  URLS
    path('add/<str:name_id>/', views.AddUserAPI.as_view(), name='AddUserAPI'),
    path('add-confirm/', views.ConfirmAddAPI.as_view(), name='ConfirmAPI'),
    path('reject/', views.RejectUserAPI.as_view(), name='RejectAPI'),

]
