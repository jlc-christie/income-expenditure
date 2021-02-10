from django.contrib.auth.models import User
from django.test import TestCase
from .models import IEStatement, Person, Address


class IEStatementTestCase(TestCase):
    def setUp(self):
        address = Address.objects.create(
            paon='1',
            street='Example Street',
            town_city='London',
            county='London',
            postcode='SW12EQ'
        )
        user = User.objects.create_user('fred', 'jlc_christie@live.com', 'abadpassword')
        user.first_name = 'Fred'
        user.last_name = 'Ives'
        user.save()
        person = Person.objects.create(user=user, address=address)
        statement = IEStatement.objects.create(
            person=person,
            salary=2500,
            income_other=500,
            mortgage=600,
            rent=0,
            utilities=200,
            travel=200,
            food=300,
            loans=500,
            credit_cards=300,
            expenditure_other=250
        )

    def test_income(self):
        statement = IEStatement.objects.get(id=1)
        self.assertEqual(statement.income, 3000)

