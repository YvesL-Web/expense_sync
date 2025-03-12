import logging

from django.db import transaction
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser


from .utils.plaid_config import plaid_config
from .models import BankAccount

logger = logging.getLogger(__name__)


class GetAllBankAccounts(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response("Nothing for th moment...coming soon.",status=status.HTTP_200_OK)


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
            institution_id = metadata.get("institution", {}).get("institution_id", "")
            institution_name = metadata.get("institution", {}).get("name", "")

            bank_account = BankAccount.objects.filter(user=request.user)
            if bank_account.filter(institution_id=institution_id).exists():
                return Response({
                    "detail": "You already linked this institution!"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Échanger le public_token contre un access_token avec Plaid
            exchange_request = ItemPublicTokenExchangeRequest(public_token)
            exchange_response = plaid_config.client.item_public_token_exchange(exchange_request)

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
