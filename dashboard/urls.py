from django.urls import path

from . import views

urlpatterns = [
    # URLS
    # Homepage Counts 
    path('messages-counts/', views.MessagesCount.as_view(), name='MessagesCountAPI'),
    path('user-counts/', views.UserCount.as_view(), name='UserCountAPI'),
    path('system-info/', views.AdminSystem.as_view(), name='AdminSystemAPI'),

    # Authentication (login, create user, logout)
    path('login/', views.LoginAPI.as_view(), name='LoginAPI'),
    path('signup/', views.CreateUser.as_view(), name='CreateUserAPI'),
    path('logout/', views.LogoutAPI.as_view(), name='LogoutAPI'),

    # logging users (saved data)
    path('logging/',views.LoggingAPI.as_view(), name='LoggingAPI'),

    # Notes
    path('notes/',views.NoteAPI.as_view(), name='NoteAPI'),
    path('notes/<int:id>/', views.DeleteNote.as_view(), name='DeleteAPIView'),

    # users api (managers management pages)
    path('users/', views.ListUserAPI.as_view(), name='ListUserAPI'),
    path('users/delete/<int:user_id>/', views.DeleteUserAPI.as_view(), name='DeleteUserAPI'),    
    path('users/block/<int:user_id>/', views.ToggleBlockUserAPI.as_view(), name='BlockUserAPI'),

    # app users 
    path('show-user/', views.ShowAppUser.as_view(), name='ShowAppUserAPI'),
    path('show-blocked-users/', views.ShowBlockedUsers.as_view(), name='ShowBlockedUserAPI'),
    path('show-inactive-users/', views.ShowInactiveUsers.as_view(), name='ShowInactiveUsersAPI'),
    path('filter-users/',views.FilterAccount.as_view(),name='FilterAccountsAPI'),

    # Appliaction Management
    path('ads-info/', views.AdsInfo.as_view(), name='AdsInfoAPI'),
    path('discount/', views.DiscountValidation.as_view(), name='DiscountValidationAPI'),
    path('ads-price/', views.AdsPrice.as_view(), name='AdsPriceAPI'),
    path('inactive-info/', views.InactiveInfo.as_view(), name='InactiveInformationAPI'),

    # Ads Managments
    path('promocode/', views.PromoCode.as_view(), name='PromoCodeAPI'),
    path('ads-requests/', views.AdsRequests.as_view(), name='AdsRequestAPI'),
    path('show-ads/', views.ShowAds.as_view(), name='ShowAdsAPI'),

    # Messages Management
    path('reports/', views.ReportsAPI.as_view(), name='ReportsAPI'),
    path('inbox/', views.InboxMessagesAPI.as_view(), name='InboxMessagesAPI'),
    path('certified-requests/', views.CertifiedRequestAPI.as_view(), name='CertifiedRequestAPI')
]
