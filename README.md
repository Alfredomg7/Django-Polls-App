# Django Polls App
This is a recreation of the Polls App from the [Django documentation](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) tutorial. The project has been customized with custom CSS styling to enhance its appearance.

## Features
- Create polls with multiple choice questions.
- Allow users to vote on polls.
- Display poll results.
- Custom CSS styling to improve the default look and feel.

## Installation
1. Clone the repository
```
git clone https://github.com/yourusername/django-polls-app.git
cd django-polls-app
```
2. Create a virtual environment (optional)
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install dependencies:
```
pip install -re requirements.txt
```
4. Apply migrations:
```
python manage.py migrate
```
5. Create a superuser
```
python manage.py createsuperuser
```
6. Run the development server:
python manage.py runserver

## Usage
1. Access the app:
Open your web browser and go to **http://127.0.0.1:8000/**.

2. Admin interface:
Go to **http://127.0.0.1:8000/admin/** to create and manage polls.

3. Vote on polls:
Users can vote on polls by selecting an option and submitting their vote.

4. View results:
After voting, users can view the results of the poll.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements
The Django Software Foundation and the Django documentation tutorial for the original project.