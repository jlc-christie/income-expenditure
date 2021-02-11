from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import FormView

from .forms import IEStatementForm, PersonForm


class CreatePersonView(FormView):
    template_name = 'registration/create.html'
    form_class = PersonForm
    success_url = reverse_lazy('login')

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class IEStatementView(LoginRequiredMixin, FormView):
    template_name = 'income_expenditure/new_statement.html'
    form_class = IEStatementForm
    success_url = reverse_lazy('new_statement')

    def form_valid(self, form):
        statement = form.save(commit=False)
        statement.person = self.request.user.person
        statement.save()
        return super().form_valid(form)


