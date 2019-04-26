from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from register.forms import RegisterForm
from register.models import RegisterRecord, Master


class RegisterView(CreateView):
    """
    Форма для регистрации
    """
    template_name = 'register/register_form.html'
    form_class = RegisterForm
    model = RegisterRecord
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно записалиь на диагностику")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'].fields['master'].queryset = Master.objects.filter(is_active=True)
        return context


