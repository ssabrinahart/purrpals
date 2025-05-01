from django.apps import AppConfig

class CatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cats'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import UserProfile
        from django.db.utils import OperationalError, ProgrammingError
        try:
            if not User.objects.filter(username='admin').exists():
                user = User.objects.create_user(
                    username='admin',
                    password='adminpass',
                    is_superuser=True,
                    is_staff=True
                )
                UserProfile.objects.create(user=user, role='Admin', gender='other')
        except (OperationalError, ProgrammingError):
            pass
