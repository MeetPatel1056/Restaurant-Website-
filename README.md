
# Restaurant Booking and Ordering System

This is a complete restaurant booking and ordering web application developed using Django, with MySQL as the production database. 
The application supports table reservations, food orders, a shopping cart, booking and order history, email notifications, and 
a contact form.

## Features

- **Table Booking**: Users can book tables at the restaurant, and booking details are automatically emailed to the user's provided email ID.
- **Order Management**: Users can place food orders, and order details are sent to their email.
- **Cart**: Users can add, update, and manage products in their cart before placing an order.
- **Booking and Order History**: Users can view their past bookings and orders.
- **Product Management**: Products can be added and managed through the backend interface.
- **Contact Us**: A functional "Contact Us" page allows users to send inquiries, which are properly handled.
- **Email Notifications**: Booking and order confirmations are sent via email to the user.
- **Database**: MySQL is used for production, while SQLite is the default for development.

## Installation

### Prerequisites
1. Python 3.8 or higher
2. Django 4.x or higher
3. MySQL server
4. Email configuration (SMTP details for sending emails)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/MeetPatel1056/Restaurant-Website-.git
   cd restaurant-booking-order
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database:
   - Update the `DATABASES` setting in `myproject/settings.py` to use your MySQL credentials.
   - Example:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'your_database_name',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000`.

## Configuration

### Email Setup
Update the email settings in `myproject/settings.py` for sending booking and order details. Example:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```

### Admin Interface
Access the Django admin interface at `http://127.0.0.1:8000/admin`. Use the superuser credentials created using:
```bash
python manage.py createsuperuser
```

## Project Structure
- `myproject/`: Main project directory with settings and configurations.
- `myapp/`: Contains the core application logic, models, views, and templates.
- `media/`: Stores uploaded files.
- `db.sqlite3`: Default development database.

## Deployment
For production, it is recommended to use:
- **Gunicorn** or **uWSGI** as the WSGI server.
- **Nginx** as the reverse proxy server.
- A **MySQL database** for better performance.
- Configure **environment variables** for sensitive data like database credentials and email settings.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to all contributors and developers for making this project possible.
