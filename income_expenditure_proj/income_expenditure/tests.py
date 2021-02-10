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
        statement = self.create_statement(person)

    @staticmethod
    def create_statement(person, salary=2500, other_income=500, mortgage=600, rent=0, utilities=200, travel=200,
                         food=300, loans=500, credit_cards=300, expenditure_other=250):
        return IEStatement.objects.create(
            person=person,
            salary=salary,
            income_other=other_income,
            mortgage=mortgage,
            rent=rent,
            utilities=utilities,
            travel=travel,
            food=food,
            loans=loans,
            credit_cards=credit_cards,
            expenditure_other=expenditure_other
        )

    def test_income(self):
        statement = IEStatement.objects.get(id=1)
        self.assertEqual(statement.income, 3000)

    def test_expenditure(self):
        statement = IEStatement.objects.get(id=1)
        self.assertEqual(statement.expenditure, 2350)

    def test_ie_ratio(self):
        statement = IEStatement.objects.get(id=1)
        self.assertAlmostEqual(statement.income_expenditure_ratio, 2350/3000)

    def test_disposable_income(self):
        statement = IEStatement.objects.get(id=1)
        self.assertEqual(statement.disposable_income, 3000-2350)

    def test_ie_ratio_grade_above_50(self):
        statement = IEStatement.objects.get(id=1)
        self.assertEqual(statement.income_expenditure_grade, 'D')

    def test_ie_ratio_grade_above_100(self):
        person = Person.objects.get(id=1)
        statement = self.create_statement(person, mortgage=2000)  # results in expenditure > income, i.e. >100% IE ratio
        self.assertEqual(statement.income_expenditure_grade, 'D')

    def test_ie_ratio_grade_C(self):
        person = Person.objects.get(id=1)
        statement = self.create_statement(person, salary=4500)  # 47% IE Ratio
        self.assertEqual(statement.income_expenditure_grade, 'C')

    def test_ie_ratio_grade_B(self):
        person = Person.objects.get(id=1)
        statement = self.create_statement(person, salary=7500)  # 29% IE Ratio
        self.assertEqual(statement.income_expenditure_grade, 'B')

    def test_ie_ratio_grade_A(self):
        person = Person.objects.get(id=1)
        statement = self.create_statement(person, salary=24500)  # 9% IE Ratio
        self.assertEqual(statement.income_expenditure_grade, 'A')

