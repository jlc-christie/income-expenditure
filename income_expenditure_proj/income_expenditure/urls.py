from django.urls import path

from .views import IEStatementView, CreatePersonView

app_name = 'income_expenditure'
urlpatterns = [
    path('statements/new', IEStatementView.as_view(), name='new_statement'),
    path('accounts/create', CreatePersonView.as_view(), name='account_create'),
]
