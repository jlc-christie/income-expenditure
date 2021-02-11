from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import FormView, ListView

from .forms import IEStatementForm, PersonForm
from .models import IEStatement


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


class IEStatementCreate(LoginRequiredMixin, FormView):
    template_name = 'income_expenditure/new_statement.html'
    form_class = IEStatementForm
    success_url = reverse_lazy('income_expenditure:new_statement')

    def form_valid(self, form):
        statement = form.save(commit=False)
        statement.person = self.request.user.person
        statement.save()
        return super().form_valid(form)


class IEStatementList(ListView):
    template_name = 'income_expenditure/statement_list.html'
    model = IEStatement
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'person'):
            return IEStatement.objects.filter(person=self.request.user.person)
        else:
            return IEStatement.objects.none()
