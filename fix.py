class GetTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        try:
            transactions_data = self.fetch_transactions(account_id, request.user)
            return Response(transactions_data, status=status.HTTP_200_OK)
        except BankAccount.DoesNotExist:
            logger.error(f"Bank account not found for user {request.user}")
            return Response({'detail': 'Bank not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in GetTransactionsView for user {request.user}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_transactions(self, account_id, user):
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

        self.apply_updates(bank, added, modified, removed, cursor)

        formatted_transactions = [{
            'transaction_id': t['transaction_id'],
            'name': t['name'],
            'payment_channel': t['payment_channel'],
            'type': t['payment_channel'],
            'account_id': t['account_id'],
            'amount': t['amount'],
            'pending': t['pending'],
            'category': t['category'][0] if t['category'] else '',
            'date': t['date'],
            'image': t.get('logo_url', '')
        } for t in added]

        return {
            "added": formatted_transactions,
            "modified": modified,
            "removed": removed,
            "cursor": cursor,
        }

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
            bank_account = BankAccount.objects.get(id=account_id, user=request.user)
            
            account_request = AccountsGetRequest(access_token=bank_account.access_token)
            account_response = plaid_config.client.accounts_get(account_request)

            transactions_view = GetTransactionsView()
            transactions_data = transactions_view.fetch_transactions(account_id, request.user)
            transactions = transactions_data["added"]

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

                for transaction in transactions:
                    if transaction.get('account_id') == acc['account_id']:
                        sub_account["transactions"].append(transaction)
                sub_accounts.append(sub_account)

            return Response({"data": sub_accounts}, status=status.HTTP_200_OK)
        
        except BankAccount.DoesNotExist:
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error in GetAccountView for user {request.user}: {str(e)}")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)