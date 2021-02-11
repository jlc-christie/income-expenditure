from django.urls import path

from .views import IEStatementCreate, CreatePersonView, IEStatementList

app_name = 'income_expenditure'
urlpatterns = [
    path('statements', IEStatementList.as_view(), name='statements'),
    path('statements/new', IEStatementCreate.as_view(), name='new_statement'),
    path('accounts/create', CreatePersonView.as_view(), name='account_create'),
]
