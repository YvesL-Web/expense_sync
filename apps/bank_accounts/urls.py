from django.urls import path
from .views import (
    GetAllBankAccounts,
    CreatePlaidLinkToken,
    ExchangePublicTokenView,
    GetAccountView,
    GetTransactionsView,
)

urlpatterns = [
    path("", GetAllBankAccounts.as_view() ),
    path("create-link-token/", CreatePlaidLinkToken.as_view()),
    path("exchange-public-token/",ExchangePublicTokenView.as_view()),
    path("get_accounts/<str:account_id>/",GetAccountView.as_view()),
    path("get_transactions/<str:account_id>/",GetTransactionsView.as_view()),
]
