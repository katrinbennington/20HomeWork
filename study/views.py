from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


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

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permisson_classes = (~IsModer)
        elif self.action in ["update", "retrieve"]:
            self.permisson_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner, ~IsModer, )
        return super().get_permissions()


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
