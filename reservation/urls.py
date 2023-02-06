from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from reservation.views import *

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('usercrud/<int:pk>/',UserdetailView.as_view()),
    path('roomtype',RoomtypeView.as_view()),
    path('roomtype/<int:pk>/',RoomtypedetailView.as_view()),
    path('rooms',RoomsView.as_view()),
    path('rooms/<int:pk>/',Roomdetailview.as_view()),
    path('reservation',BookingView.as_view()),
    path('reservation/<int:id>/',Bookingdetailview.as_view())

]