from django.contrib.auth.models import User
from .models import UserProfile
from django.db.utils import OperationalError, ProgrammingError

def create_default_admin():
    try:
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_user(
                username='admin',
                password='adminpass',
                is_superuser=True,
                is_staff=True
            )
            UserProfile.objects.create(user=user, role='admin', gender='Prefer not to say')
    except (OperationalError, ProgrammingError):
        pass  # migrations not ready yet

create_default_admin()
