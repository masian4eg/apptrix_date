from django.urls import path
from .views import (
    my_profile_view,
    ProfileView,
    match_received_view,
    accept_match,
    reject_match,
    ProfileListView,
    send_match,
    remove_match,
)

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('<int:pk>', ProfileView.as_view(), name='profile-client'),
    path('my_match/', match_received_view, name='my-match-view'),
    path('my_match/accept/', accept_match, name='accept-match'),
    path('my_match/reject/', reject_match, name='reject-match'),
    path('all_profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('send_match/', send_match, name='send-match'),
    path('remove_match/', remove_match, name='remove-match'),
]
