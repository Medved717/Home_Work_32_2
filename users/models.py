from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from educations.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите адрес электронной почты.",
    )
    phone = models.CharField(
        max_length=25,
        verbose_name="Телефон",
        help_text="Введите номер телефона.",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город проживания",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        verbose_name="Аватар",
        help_text="Загрузите аватар.",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)


class Payment(models.Model):
    CASH = 'CA'
    NON_CASH = 'NO'

    METHOD_PAY = (
        (CASH, 'Наличные'),
        (NON_CASH, 'Карта')
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='payments')
    pay_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, verbose_name='Оплаченный курс', on_delete=models.SET_NULL,
                                    related_name='course_payments', blank=True, null=True)
    paid_lesson = models.ForeignKey(Lesson, verbose_name='Оплаченный урок', on_delete=models.SET_NULL,
                                    related_name='lesson_payments', blank=True, null=True)
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты',
                                                 validators=[MinValueValidator(1), MaxValueValidator(10_000_000)])
    payment_method = models.CharField(max_length=2, verbose_name='Способ оплаты', choices=METHOD_PAY)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('user',)

    def __str__(self):
        return f'Оплата от: {self.user} на сумму {self.payment_amount}'


class Pay(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Сумма',
        help_text='Введите сумму платежа.'
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии",
        help_text="Введите ID сессии.",
        blank=True,
        null=True
    )
    link_on_pay = models.URLField(
        max_length=500,
        verbose_name="Ссылка на оплату",
        help_text="Внесите ссылку на оплату",
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return self.amount

