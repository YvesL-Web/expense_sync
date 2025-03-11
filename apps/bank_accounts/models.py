from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.utils.common_to_each_model import TimeStampedModel

User = get_user_model()

class BankAccount(TimeStampedModel):
    user = models.ForeignKey(User, related_name='bank_accounts' ,on_delete=models.CASCADE)
    # L'access_token fourni par Plaid pour accéder aux données bancaires
    access_token = models.CharField(
        unique=True,
        max_length=255,
        help_text=_("The access token associated with the Item data is being requested for."),
    )
    # L'ID de l'item Plaid (optionnel, mais utile pour référence)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    # L'institution bancaire (par exemple, "Bank of America")
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    # L'ID de l'institution bancaire (fourni par Plaid)
    institution_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Account {self.institution_name} - {self.user.email}"
    
    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"