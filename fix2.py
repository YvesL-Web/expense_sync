class GetTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        """
        Fetch and update transactions in the database for the given account_id.
        """
        try:
            # Fetch and update transactions in the database
            self.fetch_transactions(account_id, request.user)
            return Response({'detail': 'Transactions successfully updated.'}, status=status.HTTP_200_OK)
        except BankAccount.DoesNotExist:
            logger.error(f"Bank account not found for user {request.user}")
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in GetTransactionsView for user {request.user}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_transactions(self, account_id, user):
        """
        Fetch transactions from the external API and update the database.
        """
        bank = BankAccount.objects.get(id=account_id, user=user)
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

        # Apply updates to the database
        self.apply_updates(bank, added, modified, removed, cursor)

    def apply_updates(self, bank, added, modified, removed, cursor) -> None:
        """
        Update the database with the fetched transactions.
        """
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
                    "image": transaction.get('logo_url', '')
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

        Transaction.objects.filter(transaction_id__in=[t['transaction_id'] for t in removed]).delete()
        SyncCursor.objects.filter(bank=bank).update(cursor=cursor)


class GetAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        try:
            # Récupérer le compte bancaire
            bank_account = BankAccount.objects.get(id=account_id, user=request.user)
            
            # Récupérer les détails du compte via Plaid
            account_request = AccountsGetRequest(access_token=bank_account.access_token)
            account_response = plaid_config.client.accounts_get(account_request)

            # Mettre à jour les transactions dans la base de données
            transactions_view = GetTransactionsView()
            transactions_view.fetch_transactions(account_id, request.user)

            # Récupérer les transactions mises à jour depuis la base de données
            transactions = Transaction.objects.filter(bank=bank_account)

            # Construire la réponse avec les sous-comptes et leurs transactions
            sub_accounts = []
            for acc in account_response.to_dict()["accounts"]:
                sub_account = {
                    'account_id': acc['account_id'],
                    'institution_id': bank_account.institution_id,
                    'name': acc['name'],
                    'official_name': acc.get('official_name', ''),
                    'type': str(acc['type']),
                    'subtype': str(acc['subtype']),
                    "transactions": []
                }

                # Associer les transactions au sous-compte correspondant
                for transaction in transactions:
                    if transaction.account_id == acc['account_id']:
                        serializer = TransactionSerializer(transaction)
                        sub_account["transactions"].append(serializer.data)
                
                sub_accounts.append(sub_account)

            return Response({"data": sub_accounts}, status=status.HTTP_200_OK)
        
        except BankAccount.DoesNotExist:
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error in GetAccountView for user {request.user}: {str(e)}")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)