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


# for acc in account_response['accounts']:
        #     account = {
        #         'account_id': acc['account_id'],
        #         'available_balance': acc['balances'].get('available', 0),
        #         'current_balance': acc['balances'].get('current', 0),
        #         'institution_id': bank_account.institution_id,
        #         'name': acc['name'],
        #         'official_name': acc.get('official_name', ''),
        #         'mask': acc['mask'],
        #         'type': str(acc['type']),  # Convert to string
        #         'subtype': str(acc['subtype']),  # Convert to string
        #         'bank_account_id': bank_account.id,
        #     }
        #     accounts.append(account)
        #     total_current_balance += account['current_balance']
