from rest_framework.serializers import ValidationError


class VideoValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video = value.get(self.field)
        if video and not video.startswith('https://www.youtube.com/'):
            raise ValidationError('Cсылки на сторонние образовательные платформы или личные сайты запрещены')
