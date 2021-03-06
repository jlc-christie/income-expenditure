from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    paon = models.CharField(max_length=80)
    saon = models.CharField(max_length=80, blank=True, default='')
    street = models.CharField(max_length=80)
    town_city = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    postcode = models.CharField(max_length=8)

    def __str__(self):
        return f"Address: <{self.paon}{', ' + self.saon if self.saon != '' else None} {self.street}, {self.postcode}>"


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class IEStatement(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # Income
    salary = models.PositiveIntegerField()
    income_other = models.PositiveIntegerField()

    # Expenditure
    mortgage = models.PositiveIntegerField()
    rent = models.PositiveIntegerField()
    utilities = models.PositiveIntegerField()
    travel = models.PositiveIntegerField()
    food = models.PositiveIntegerField()
    loans = models.PositiveIntegerField()
    credit_cards = models.PositiveIntegerField()
    expenditure_other = models.PositiveIntegerField()

    @property
    def income(self):
        return self.salary + self.income_other

    @property
    def expenditure(self):
        return sum([self.mortgage, self.rent, self.utilities, self.travel, self.food, self.loans, self.credit_cards,
                    self.expenditure_other])

    @property
    def income_expenditure_ratio(self, percentage=True):
        return self.expenditure / self.income

    @property
    def income_expenditure_grade(self):
        ratio = self.income_expenditure_ratio
        if ratio < 0.1:
            return 'A'
        elif ratio < 0.3:
            return 'B'
        elif ratio < 0.5:
            return 'C'
        else:
            return 'D'

    @property
    def disposable_income(self):
        return self.income - self.expenditure
