from rest_framework.exceptions import ValidationError


class InvalidLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        valid_link = 'youtube.com'
        if value.get('link_on_video'):
            if valid_link not in value.get('link_on_video'):
                raise ValidationError('Введена недопустимая ссылка!')
        return value