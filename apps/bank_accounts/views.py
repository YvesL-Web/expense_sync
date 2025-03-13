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

from apps.bank_accounts.serializers import BankAccountSerializer


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
            total_current_balance = 0
            # Retrieve account details from Plaid
            for bank_account in bank_accounts:
                account_request = AccountsGetRequest(
                    access_token=bank_account.access_token)
                account_response = plaid_config.client.accounts_get(
                    account_request)

                for acc in account_response['accounts']:
                    account = {
                        'account_id': acc['account_id'],
                        'available_balance': acc['balances'].get('available', 0),
                        'current_balance': acc['balances'].get('current', 0),
                        'institution_id': bank_account.institution_id,
                        'name': acc['name'],
                        'official_name': acc.get('official_name', ''),
                        'mask': acc['mask'],
                        'type': str(acc['type']),  # Convert to string
                        'subtype': str(acc['subtype']),  # Convert to string
                        'bank_account_id': bank_account.id,
                    }
                    accounts.append(account)
                    total_current_balance += account['current_balance']

            # Construct response
            response_data = {
                "accounts": accounts,
                "total_banks": len(accounts),
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
            # Récupérer la banque depuis la base de données
            bank_account = BankAccount.objects.get(
                id=account_id, user=request.user)
            # Récupérer les informations du compte depuis Plaid
            account_request = AccountsGetRequest(
                access_token=bank_account.access_token, )
            account_response = plaid_config.client.accounts_get(
                account_request)

            account_data = account_response.to_dict()["accounts"][0]

            # Récupérer les transactions depuis Plaid
            transactions_request = TransactionsSyncRequest(
                access_token=bank_account.access_token)
            transactions_response = plaid_config.client.transactions_sync(
                transactions_request)

            # Récupérer les transactions depuis la base de données
            transactions = Transaction.objects.filter(bank=bank_account)
            # transactions = Transaction.objects.filter(bank=bank_account).values()

            # Récupérer les transactions synchronisées
            sync_transactions = self.get_transaction(
                bank_account.access_token, bank_account.item_id)

            # Construire l'objet compte
            account = {
                'account_id': account_data['account_id'],
                'available_balance': account_data['balances']['available'],
                'current_balance': account_data['balances']['current'],
                'institution_id': bank_account.institution_id,
                'name': account_data['name'],
                'official_name': account_data['official_name'],
                'mask': account_data['mask'],
                'type': account_data['type'],
                'subtype': account_data['subtype'],
                'bank_account_id': bank_account.id,
            }

            print(f"Synchronised transactions: {sync_transactions}")
            print(f"Database transactions values: {transactions}")

            # Fusionner et trier les transactions
            all_transactions = list(transactions) + sync_transactions
            all_transactions.sort(key=lambda x: x['date'], reverse=True)

            return Response({
                "data": account,
                "transactions": all_transactions
            }, status=status.HTTP_200_OK)
        except BankAccount.DoesNotExist:
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Something went wrong in GetAccountView for user {self.request.user} -> {str(e)}")
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def get_transaction(self, access_token, item_id):
        # Récupérer le cursor depuis la base de données
        sync_cursor = SyncCursor.objects.filter(bank__item_id=item_id).first()
        cursor = sync_cursor.cursor if sync_cursor else ""

        transactions = []
        has_more = True

        # Synchroniser les transactions
        while has_more:
            transaction_request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=cursor if cursor else "",
            )
            transaction_response = plaid_config.client.transactions_sync(
                transaction_request)

            # Ajouter les transactions synchronisées
            transactions.extend(transaction_response["added"])

            # Mettre à jour le curseur
            cursor = transaction_response["next_cursor"]
            has_more = transaction_response["has_more"]

        # Formater les transactions
        formatted_transactions = [{
            'id': t['transaction_id'],
            'name': t['name'],
            'payment_channel': t['payment_channel'],
            'type': t['payment_channel'],
            'account_id': t['account_id'],
            'amount': t['amount'],
            'pending': t['pending'],
            'category': t['category'][0] if t['category'] else '',
            'date': t['date'],
            'image': t['logo_url'],
        } for t in transactions]

        return formatted_transactions


class GetTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        try:
            # Récupérer le cursor depuis la base de données
            bank = BankAccount.objects.get(id=account_id, user=request.user)
            sync_cursor, created = SyncCursor.objects.get_or_create(bank=bank)
            cursor = sync_cursor.cursor

            # Variables pour stocker les transactions synchronisées
            added = []
            modified = []
            removed = []
            has_more = True

            # Synchroniser les transactions
            while has_more:
                transaction_request = TransactionsSyncRequest(
                    access_token=bank.access_token,
                    cursor=cursor if cursor else "",
                )
                transaction_response = plaid_config.client.transactions_sync(
                    transaction_request)

                # Ajouter les transactions synchronisées
                added.extend(transaction_response["added"])
                modified.extend(transaction_response["modified"])
                removed.extend(transaction_response["removed"])

                # Mettre à jour le curseur
                cursor = transaction_response["next_cursor"]
                has_more = transaction_response["has_more"]

            # fonction pour appliquer les mises à jour dans la base de données
            self.apply_updates(bank, added, modified, removed, cursor)

            # Formater les transactions pour la réponse
            formatted_transactions = [{
                'id': t['transaction_id'],
                'name': t['name'],
                'payment_channel': t['payment_channel'],
                'type': t['payment_channel'],
                'account_id': t['account_id'],
                'amount': t['amount'],
                'pending': t['pending'],
                'category': t['category'][0] if t['category'] else '',
                'date': t['date'],
                'image': t['logo_url'],
            } for t in added]

            return Response({
                "added": formatted_transactions,
                "modified": modified,
                "removed": removed,
                "cursor": cursor,
            }, status=status.HTTP_200_OK)

        except BankAccount.DoesNotExist:
            logger.error(
                f"Something went wrong in GetTransactionsView for user {self.request.user} -> {str(e)}")
            return Response({'detail': 'Bank not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Something went wrong in GetTransactionsView for user {self.request.user} -> {str(e)}")
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def apply_updates(self, bank, added, modified, removed, cursor) -> None:
        # Appliquer les transactions ajoutées
        for transaction in added:
            Transaction.objects.update_or_create(
                transaction_id=transaction['transaction_id'],
                defaults={
                    'bank': bank,
                    'name': transaction['name'],
                    'amount': transaction['amount'],
                    'date': transaction['date'],
                    'pending': transaction['pending'],
                    'category': transaction['category'][0] if transaction['category'] else '',
                    'payment_channel': transaction['payment_channel'],
                }
            )

        # Appliquer les transactions modifiées
        for transaction in modified:
            Transaction.objects.filter(transaction_id=transaction['transaction_id']).update(
                name=transaction['name'],
                amount=transaction['amount'],
                date=transaction['date'],
                pending=transaction['pending'],
                category=transaction['category'][0] if transaction['category'] else '',
                payment_channel=transaction['payment_channel'],
            )

        # Supprimer les transactions supprimées
        Transaction.objects.filter(transaction_id__in=removed).delete()
        # for transaction in removed:
        #     Transaction.objects.filter(transaction_id=transaction['transaction_id']).delete()

        # Mettre à jour le curseur
        SyncCursor.objects.filter(bank=bank).update(cursor=cursor)
        # SyncCursor.objects.update(bank=bank, cursor=cursor)
