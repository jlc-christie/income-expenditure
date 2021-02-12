from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import FormView, ListView, DetailView

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


class IEStatementList(LoginRequiredMixin, ListView):
    template_name = 'income_expenditure/statement_list.html'
    model = IEStatement
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_queryset().count() > 0:
            context['latest_statement'] = self.get_queryset().latest('id')
        return context

    def get_queryset(self):
        if hasattr(self.request.user, 'person'):
            return IEStatement.objects.filter(person=self.request.user.person).order_by('-id')
        else:
            return IEStatement.objects.none()


class IEStatementDetail(UserPassesTestMixin, DetailView):
    template_name = 'income_expenditure/statement_detail.html'
    model = IEStatement

    def test_func(self):
        statement = self.get_object()
        person = self.request.user.person if hasattr(self.request.user, 'person') else None
        return statement.person == person
