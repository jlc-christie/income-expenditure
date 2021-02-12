# I&E Tracker
Simple Django Web App to submit Income & Expenditure Statements, returning Income-to-Expenditure Ratio, Disposable Income and a Rating/Grade based on the Ratio. Bootstrap was used to style the UI for simplicity. Django Secret Key and sqlite db were commited as this is a test project and won't be used in any kind of production environment. This means the project can simply be run without applying migrations, etc. 

## Setup 
The project uses pipenv, assuming you have pipenv installed:
1. Clone project: `git clone https://github.com/jlc-christie/income-expenditure.git`
2. Install requirements in pipenv environment: `pipenv install`
3. Start test server (defaults to port 8000): `pipenv run python manage.py runserver`
4. Open in browser: `http://localhost:8000`
