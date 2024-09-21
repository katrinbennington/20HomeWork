from django.urls import path

from study.apps import StudyConfig
from rest_framework.routers import DefaultRouter

from study.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                         LessonUpdateAPIView, LessonDestroyAPIView,
                         SubscriptionViewSet)

app_name = StudyConfig.name

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
              ] + router.urls
