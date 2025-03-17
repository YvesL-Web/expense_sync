import logging

from django.db import transaction
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from apps.bank_accounts.serializers import BankAccountSerializer, TransactionSerializer


from .utils.plaid_config import plaid_config
from .models import BankAccount, SyncCursor, Transaction

logger = logging.getLogger(__name__)


class GetAllBankAccounts(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_banksAccount = BankAccount.objects.filter(user=user)
        return Response(BankAccountSerializer(user_banksAccount, many=True).data, status=status.HTTP_200_OK)


class CreatePlaidLinkToken(APIView):
    """
    Create a link_token and pass the temporary token to your app's client.
    https://plaid.com/docs/api/tokens/#linktokencreate
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            link_request = LinkTokenCreateRequest(
                products=plaid_config.products,
                client_name=plaid_config.client_name,
                country_codes=plaid_config.country_codes,
                language=plaid_config.language,
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(self.request.user.id))
            )

            response = plaid_config.client.link_token_create(link_request)
            return Response(response.to_dict(), status=201)
        except Exception as e:
            logger.error(
                f"Something went wrong in CreatePlaidLinkToken for user {self.request.user} -> {str(e)}")
            return Response({}, status=500)


class ExchangePublicTokenView(APIView):
    """
    Exchange the public_token for a permanent access_token and item_id.
    https://plaid.com/docs/api/items/#itempublic_tokenexchange
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:

            public_token = request.data.get("public_token")
            metadata = request.data.get("metadata")
            institution_id = metadata.get(
                "institution", {}).get("institution_id", "")
            institution_name = metadata.get("institution", {}).get("name", "")

            bank_account = BankAccount.objects.filter(user=request.user)
            if bank_account.filter(institution_id=institution_id).exists():
                return Response({
                    "detail": "You already linked this institution!"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Échanger le public_token contre un access_token avec Plaid
            exchange_request = ItemPublicTokenExchangeRequest(public_token)
            exchange_response = plaid_config.client.item_public_token_exchange(
                exchange_request)

            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']

            # Créer un nouveau compte dans la base de données
            new_account = BankAccount.objects.create(
                user=request.user,
                access_token=access_token,
                item_id=item_id,
                institution_name=institution_name,
                institution_id=institution_id,
            )

            return Response({
                "detail": "Account successfully linked."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                f"Something went wrong in ExchangePublicAccessToken for user {self.request.user} -> {str(e)}")
            return Response({
                "detail": "Something went wrong while integrating your bank account."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAccountsView(APIView):
    """
    API view to fetch and return bank account details linked to the authenticated user.
    - Fetches accounts from the database.
    - Retrieves real-time account details from Plaid.
    - Computes total current balance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            # Fetch user bank accounts (Database Hit: 1)
            bank_accounts = BankAccount.objects.filter(
                user=user).only('id', 'access_token', 'institution_id')

            accounts = []
            current_balance = 0
            # Retrieve account details from Plaid
            for bank_account in bank_accounts:
                account_request = AccountsGetRequest(
                    access_token=bank_account.access_token)
                account_response = plaid_config.client.accounts_get(
                    account_request)
                
                
                for acc in account_response['accounts']:
                    current_balance += acc['balances'].get('current', 0)
                # construct account object
                account = {
                    'bank_account_id': bank_account.id,
                    'institution_id': bank_account.institution_id,
                    "available_balance": current_balance,
                    "institution_name": bank_account.institution_name,
                }
                accounts.append(account)

            # Construct response
            total_current_balance= sum(account['available_balance'] for account in accounts)
            response_data = {
                "accounts": accounts,
                "total_banks": len(bank_accounts),
                "total_current_balance": total_current_balance,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"Error in GetAccountsView for user {request.user}: {str(e)}")
            return Response({"detail": "Could not retrieve accounts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        try:
            bank_account = BankAccount.objects.get(id=account_id, user=request.user)
            
            account_request = AccountsGetRequest(access_token=bank_account.access_token)
            account_response = plaid_config.client.accounts_get(account_request)

            GetTransactionsView().get(request, account_id)  # Corrected method call
            
            transactions = Transaction.objects.filter(bank=bank_account)


            sub_accounts = []
            for acc in account_response.to_dict()["accounts"]:  # Ensure correct dict access
                sub_account = {
                    'account_id': acc['account_id'],
                    'institution_id': bank_account.institution_id,
                    'name': acc['name'],
                    'official_name': acc.get('official_name', ''),
                    'type': str(acc['type']),
                    'subtype': str(acc['subtype']),
                    "transactions": []
                }

                for transaction in transactions:
                    serializer = TransactionSerializer(transaction)
                    serializer_data = serializer.data
                    if serializer_data.get('account_id') == acc['account_id']:  # Fix potential error
                        sub_account["transactions"].append(serializer_data)
                sub_accounts.append(sub_account)

            return Response({"data": sub_accounts}, status=status.HTTP_200_OK)
        
        except BankAccount.DoesNotExist:
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error in GetAccountView for user {self.request.user}: {str(e)}")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        try:
            bank = BankAccount.objects.get(id=account_id, user=request.user)
            sync_cursor, created = SyncCursor.objects.get_or_create(bank=bank)
            cursor = sync_cursor.cursor

            added, modified, removed = [], [], []
            has_more = True

            while has_more:
                transaction_request = TransactionsSyncRequest(
                    access_token=bank.access_token, cursor=cursor or ""
                )
                transaction_response = plaid_config.client.transactions_sync(transaction_request)

                added.extend(transaction_response["added"])
                modified.extend(transaction_response["modified"])
                removed.extend(transaction_response["removed"])

                cursor = transaction_response["next_cursor"]
                has_more = transaction_response["has_more"]

            self.apply_updates(bank, added, modified, removed, cursor)

            formatted_transactions = [{
                'transaction_id': t['transaction_id'],
                'name': t['name'],
                'payment_channel': t['payment_channel'],
                'type': t['payment_channel'],
                'account_id': t['account_id'], # Fix missing key issue
                'amount': t['amount'],
                'pending': t['pending'],
                'category': t['category'][0] if t['category'] else '',
                'date': t['date'],
                'image': t.get('logo_url', '')  # Fix missing key issue
            } for t in added]
            
            logger.info(f"Transactions fetched for user {self.request.user}")
            return Response({
                "added": formatted_transactions,
                "modified": modified,
                "removed": removed,
                "cursor": cursor,
            }, status=status.HTTP_200_OK)

        except BankAccount.DoesNotExist:
            logger.error(f"Bank account not found for user {self.request.user}")
            return Response({'detail': 'Bank not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error in GetTransactionsView for user {self.request.user}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def apply_updates(self, bank, added, modified, removed, cursor) -> None:
        for transaction in added:
            Transaction.objects.update_or_create(
                transaction_id=transaction['transaction_id'],
                defaults={
                    'bank': bank,
                    "account_id": transaction['account_id'],
                    'name': transaction['name'],
                    'amount': transaction['amount'],
                    'date': transaction['date'],
                    'pending': transaction['pending'],
                    'category': transaction['category'][0] if transaction['category'] else '',
                    'payment_channel': transaction['payment_channel'],
                    "image": transaction.get('logo_url', '')  # Fix missing key issue
                }
            )

        for transaction in modified:
            Transaction.objects.filter(transaction_id=transaction['transaction_id']).update(
                name=transaction['name'],
                amount=transaction['amount'],
                date=transaction['date'],
                pending=transaction['pending'],
                category=transaction['category'][0] if transaction['category'] else '',
                payment_channel=transaction['payment_channel'],
            )

        # Correct removal handling
        Transaction.objects.filter(transaction_id__in=[t['transaction_id'] for t in removed]).delete()

        SyncCursor.objects.filter(bank=bank).update(cursor=cursor)