from django.urls import path

from .views import AdvertisementView, AdvertisementsView, AdvertisementsByTagsView, AdvertisementCreatView, RegisterView, UserView, UsersAdvetisementsView

urlpatterns = [
    path('advertisements/', AdvertisementsView.as_view()),
    path('advertisements/byTags/', AdvertisementsByTagsView.as_view()),
    path('advertisement/create/', AdvertisementCreatView.as_view()),
    path('advertisement/<int:id>/', AdvertisementView.as_view()),
    path('user/create/', RegisterView.as_view()),
    path('user/advertisements/', UsersAdvetisementsView.as_view()),
    path('user/<str:username>/', UserView.as_view()),
]
