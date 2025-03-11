from django.urls import path
from .views import (
    GetAllBankAccounts,
    CreatePlaidLinkToken,
    ExchangePublicTokenView
)


urlpatterns = [
    path("", GetAllBankAccounts.as_view() ),
    path("create-link-token/", CreatePlaidLinkToken.as_view()),
    path("exchange-public-token/",ExchangePublicTokenView.as_view())
]
