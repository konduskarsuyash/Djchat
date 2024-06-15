from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/server/select', ServerListViewSet, basename='server')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/ui/', SpectacularSwaggerView.as_view()),
]+router.urls