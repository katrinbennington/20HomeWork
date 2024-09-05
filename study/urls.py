from django.urls import path

from study.apps import StudyConfig
from rest_framework.routers import DefaultRouter

from study.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                         LessonUpdateAPIView, LessonDestroyAPIView)

app_name = StudyConfig.name


router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='moto-create'),
    path('lesson/list/', LessonListAPIView.as_view(), name='moto-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='moto-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='moto-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='moto-delete'),
] + router.urls
