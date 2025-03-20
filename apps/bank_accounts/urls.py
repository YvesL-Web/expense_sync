from django.urls import path, re_path
from .views import (
    GetAllBankAccounts,
    CreatePlaidLinkToken,
    ExchangePublicTokenView,
    GetAccountView,
    GetTransactionsView,
    GetAccountsView,
    GetAccountTransactions
)

urlpatterns = [
    path("", GetAllBankAccounts.as_view() ),
    path("create-link-token/", CreatePlaidLinkToken.as_view()),
    path("exchange-public-token/",ExchangePublicTokenView.as_view()),
    path("get_accounts/",GetAccountsView.as_view()),
    re_path(r"^get_account_transactions/(?P<account_id>[0-9a-fA-F-]+)?$", GetAccountTransactions.as_view()),
    path("get_accounts/<str:account_id>/",GetAccountView.as_view()),
    path("get_transactions/<str:account_id>/",GetTransactionsView.as_view()),
]
