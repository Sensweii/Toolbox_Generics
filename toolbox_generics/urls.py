from django.contrib import admin
from django.urls import include
from django.urls import path

from oauth2_provider.views import TokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),
    path('token/', TokenView.as_view()),
]
