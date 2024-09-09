from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson, Subscription
from study.validators import VideoValidator


class CourseSerializer(ModelSerializer):
    lessons = serializers.SerializerMethodField()
    validators = [VideoValidator(field='video')]
    is_subscription = serializers.SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscription(self, course):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, user=user.id)
        if subscription:
            return True
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)
    validators = [VideoValidator(field='video')]


    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_with_same_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lessons", many=True)

    def get_count_lesson_with_same_course(self, obj):
        return obj.lessons.all().count()

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            course = obj
            subscription = Subscription.objects.filter(course=course, user=user).first()
            if subscription:
                return subscription.status
        return False

    class Meta:
        model = Course
        fields = ("name", "description", "count_lesson_with_same_course", "lesson")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
