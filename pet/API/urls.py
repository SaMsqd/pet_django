from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


router = SimpleRouter()
router.register(r'films', views.FilmAll, basename='films')
router.register(r'reviews', views.ReviewAll, basename='reviews')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', views.UserMe.as_view()),
    path('v1/', include(router.urls)),
]
