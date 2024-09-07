from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_with_same_course = SerializerMethodField()
    lesson = LessonSerializer(source="lessons", many=True)

    def get_count_lesson_with_same_course(self, obj):
        return obj.lessons.all().count()

    class Meta:
        model = Course
        fields = ("name", "description", "count_lesson_with_same_course", "lesson")
