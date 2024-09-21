from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.tasks import sub_update

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from study.models import Course, Lesson, Subscription
from study.paginators import CoursePaginator, LessonPaginator
from study.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """CourseViewSet endpoint"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = (~IsModerator,)
    #     elif self.action in ['update', 'retrieve']:
    #         self.permission_classes = (IsModerator | IsOwner,)
    #     elif self.action == 'destroy':
    #         self.permission_classes = (IsOwner | ~IsModerator,)
    #     return super().get_permissions()

    def update(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            sub_update.delay(pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateAPIView(CreateAPIView):
    """LessonCreateAPIView endpoint"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """LessonListAPIView endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    """LessonRetrieveAPIView endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    """LessonUpdateAPIView endpoint"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    """LessonDestroyAPIView endpoint"""

    def get_queryset(self):
        if IsModer().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsOwner | ~IsModer]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """SubscriptionViewSet endpoint"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Вы отписались'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Вы подписались'
        return Response({"message": message})
