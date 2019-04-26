from django import forms
from django.core.exceptions import ValidationError

from register.models import RegisterRecord, Schedule


class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class RegisterForm(forms.ModelForm):
    """Форма записи на диагностику"""

    client_fio = forms.CharField(label='Ф.И.О', max_length=256)
    date = forms.DateTimeField(label='Дата и время посещения', input_formats=['%Y-%m-%dT%H:%M'],
                               widget=MyDateTimeInput())

    class Meta:
        model = RegisterRecord
        fields = '__all__'

    def clean(self):
        master = self.cleaned_data.get('master')
        date = self.cleaned_data.get('date')
        if master and date and RegisterRecord.objects.filter(master=master, date__hour=date.hour).exists():
            raise ValidationError("Выбранный мастер уже занят на это время")
        if date and not Schedule.check_date(date):
            shdl = Schedule.get_day_schedule(date)
            if shdl[0]:
                message = "Выбрано нерабочее время. Время работы в этот день: {0}-{1}".format(
                    shdl[1].strftime("%H:%M"), shdl[2].strftime("%H:%M"))
            else:
                message = "Выбран нерабочий день"
            raise ValidationError(message)
