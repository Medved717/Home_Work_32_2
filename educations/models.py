from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса.",
    )
    preview = models.ImageField(
        upload_to="educations/media/preview",
        verbose_name="Изображение курса",
        help_text="Загрузите изображение урока",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание.", blank=True, null=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("title",)


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название предмета",
        help_text="Введите название предмета",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание предмета."
    )
    preview = models.ImageField(
        upload_to="educations/media/preview",
        verbose_name="Изображение курса",
        help_text="Загрузите изображение курса",
        blank=True,
        null=True,
    )
    link_on_video = models.CharField(
        max_length=300,
        verbose_name="Ссылка на видео",
        help_text="Загрузите ссылку на видео.",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        on_delete=models.SET_NULL,
        related_name="lessons",
        null=True,
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Владелец урока', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("title",)


class Subscriptions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Подписка пользователя', on_delete=models.CASCADE,
                             related_name='user_subscriptions')
    course = models.ForeignKey(Course, verbose_name='Курс подписки', on_delete=models.CASCADE,
                               related_name='subscriptions_user')


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)

    def __str__(self):
        return f'Подписка пользователя {self.user}, к курсу {self.course}'
