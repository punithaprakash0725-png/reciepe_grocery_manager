# MealMate — Recipe & Grocery List Manager

## Features
- Public recipe vault
- User registration/login
- User recipe submissions (admin approval required)
- Weekly meal planner (Monday–Sunday; breakfast/lunch/dinner)
- Grocery list aggregated from the user's planned recipes
- Django admin dashboard for managing recipes, users, and meal plans

## Run in VS Code
1. Open this folder in VS Code.
2. Open Terminal in VS Code.
3. Create and activate a virtual environment:
   - Windows: `py -m venv venv` then `venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create database tables: `python manage.py makemigrations planner` then `python manage.py migrate`
6. Create admin account: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`
8. Open `http://127.0.0.1:8000/`

## Roles
- Normal user: register from the website.
- Admin: create using `createsuperuser`; log in at `/admin/` or use the Admin panel link.
- Admin approves submitted recipes in `/admin/` by setting `is_approved`.

## Important next improvements
- Add edit/delete controls for the user's own recipes and meal plans.
- Add quantity-aware ingredient parsing (current version groups by ingredient name but preserves each entered quantity).
- Add automated tests, deployment settings, and secure production secret handling.
