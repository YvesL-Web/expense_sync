import logging
from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender: Type[Model], instance:Model, created:bool, **kwargs: Any) -> None:
    
    if created:
        try:
            Profile.objects.get(user=instance)
        except:
            Profile.objects.create(user=instance)
            logger.info(f"Profile created for {instance.first_name} {instance.last_name}.")
    else:
        pass