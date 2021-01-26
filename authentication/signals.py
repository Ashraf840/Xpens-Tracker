from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver


# NB:
# THIS FILE NEEDS TO BE IMPORTED in the apps.py file, 
# & install this project-app by using the exact same name "authentication.apps.AuthenticationConfig" 
# inside the INSTALLED_APPS of 'settings.py' to make it functional.


# newly created user will be automatically inactive, so they can't login without executing account activation through email
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        print("Creating Inactive User")
        instance.is_active = False
    else:
        print("Updating User Record")