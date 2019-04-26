from django.core.exceptions import ValidationError
from django.db import models

from model_utils import Choices


class Master(models.Model):
    """
    Мастер по диагностике
    """
    name = models.CharField('Имя', max_length=256)
    is_active = models.BooleanField('Доступен для выбора', default=True)

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    """
    Справочник марок автомобилей
    """
    name = models.CharField('Марка', max_length=128)

    class Meta:
        verbose_name = 'Марка машины'
        verbose_name_plural = 'Марки машин'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
    Справочник моделей автомобилей
    """
    brand = models.ForeignKey(CarBrand, verbose_name='Марка', on_delete=models.PROTECT)
    name = models.CharField('Название модели', max_length=128)

    class Meta:
        verbose_name = 'Модель машины'
        verbose_name_plural = 'Модели машин'

    def __str__(self):
        return  self.name


class Schedule(models.Model):
    """
    Расписание работы на неделю
    """
    WEEKDAY_CHOICES = Choices(
        (0, 'MONDAY', 'Понедельник'),
        (1, 'TUESDAY', 'Вторник'),
        (2, 'WEDNESDAY', 'Среда'),
        (3, 'THURSDAY', 'Четверг'),
        (4, 'FRIDAY', 'Пятница'),
        (5, 'SATURDAY', 'Суббота'),
        (6, 'SUNDAY', 'Воскресенье')
    )

    weekday = models.IntegerField('День недели', choices=WEEKDAY_CHOICES, unique=True)
    is_workday = models.BooleanField('Рабочий день', default=True, )
    begin = models.TimeField('Начало рабочего дня', blank=True, null=True)
    end = models.TimeField('Конец рабочего дня', blank=True, null=True)

    class Meta:
        verbose_name = 'Режим работы'
        verbose_name_plural = 'Режим работы'
        ordering = ('weekday',)

    def __str__(self):
        return str(self.WEEKDAY_CHOICES[self.weekday])

    @classmethod
    def check_date(cls, date):
        """
        Проверяет попадает ли дата в рабочее время
        :param date: datetime
        :return: bool
        """
        return cls.objects.filter(weekday=date.weekday(), is_workday=True, begin__lte=date, end__gt=date).exists()

    @classmethod
    def get_day_schedule(cls, date):
        """
        Возвращает расписание работы на день, в виде кортежа
        (<флаг>, <время_начала_работы>, <время_окончания_работы>)
        <флаг> - является ли день рабочим
        :param date: datetime
        :return: tuple (bool, time(), time())
        """
        shdl_day = cls.objects.get(weekday=date.weekday())
        res = (shdl_day.is_workday, shdl_day.begin, shdl_day.end)
        return res


class RegisterRecord(models.Model):
    """
    Записи на диагностику
    """
    client_fio = models.CharField('Клиент', max_length=256)
    date = models.DateTimeField('Дата и время')
    master = models.ForeignKey(Master, on_delete=models.PROTECT, verbose_name='Мастер')
    car_brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, verbose_name='Марка')
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, verbose_name='Модель')

    class Meta:
        verbose_name = 'Запись на диагностику'
        verbose_name_plural = 'Записи на диагностику'
        ordering = ('-date',)

    def __str__(self):
        return ''.join((self.client_fio, ' (', str(self.car_model), ')'))
