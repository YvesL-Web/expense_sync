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

            # account_data = account_response.to_dict()["accounts"][0]

            # Récupérer les transactions depuis Plaid
            trans = self.get_transactions(request.user, account_id)
            print(f"Transactions: {trans}")
            # Récupérer les transactions depuis Plaid
            # transactions_request = TransactionsSyncRequest(
            #     access_token=bank_account.access_token)
            # transactions_response = plaid_config.client.transactions_sync(
            #     transactions_request)

            # # Récupérer les transactions depuis Plaid
            # get_transactions(request, account_id)

            # Récupérer les transactions depuis la base de données
            transactions = Transaction.objects.filter(bank=bank_account)
        
            # Construire l'objet compte
            # account = {
            #     'account_id': account_data['account_id'],
            #     'available_balance': account_data['balances']['available'],
            #     'current_balance': account_data['balances']['current'],
            #     'institution_id': bank_account.institution_id,
            #     'name': account_data['name'],
            #     'official_name': account_data['official_name'],
            #     'mask': account_data['mask'],
            #     'type': account_data['type'],
            #     'subtype': account_data['subtype'],
            #     'bank_account_id': bank_account.id,
            # }
            sub_accounts = []
            for acc in account_response['accounts']:
                sub_account = {
                    'account_id': acc['account_id'],
                    'institution_id': bank_account.institution_id,
                    'name': acc['name'],
                    'official_name': acc.get('official_name', ''),
                    'type': str(acc['type']),  # Convert to string
                    'subtype': str(acc['subtype']),  # Convert to string
                    "transactions": []
                }

                for transaction in transactions:
                    serializer = TransactionSerializer(transaction)
                    if serializer.data['account_id'] == acc['account_id']:
                        sub_account["transactions"].append(serializer.data)
                sub_accounts.append(sub_account)

            print(f"Database transactions values: {transactions}")

            # # Fusionner et trier les transactions
            # all_transactions = list(transactions) + sync_transactions
            # all_transactions.sort(key=lambda x: x['date'], reverse=True)

            return Response({
                "data": sub_accounts,
                # "transactions": transactions
            }, status=status.HTTP_200_OK)
        except BankAccount.DoesNotExist:
            return Response({'detail': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Something went wrong in GetAccountView for user {self.request.user} -> {str(e)}")
            return Response([], status=status.HTTP_404_NOT_FOUND)
        
    def get_transactions(self, user, account_id):
        try:
            # Récupérer le cursor depuis la base de données
            bank = BankAccount.objects.get(id=account_id, user=user)
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
            self.apply_transactions_updates(bank, added, modified, removed, cursor)

            print(f"Added transactions: {added}")

            # Formater les transactions pour la réponse
            formatted_transactions = [{
                'id': t['id'],
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
                f"Something went wrong in GetTransactionsView for user {user} -> {str(e)}")
            return Response({'detail': 'Bank not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f"Something went wrong in GetTransactionsView for user {user} -> {str(e)}")
            return Response([], status=status.HTTP_404_NOT_FOUND)


    def apply_transactions_updates(self,bank, added, modified, removed, cursor) -> None:
        # Appliquer les transactions ajoutées
        for transaction in added:
            Transaction.objects.update_or_create(
                id=transaction['id'],
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
            Transaction.objects.filter(id=transaction['id']).update(
                name=transaction['name'],
                amount=transaction['amount'],
                date=transaction['date'],
                pending=transaction['pending'],
                category=transaction['category'][0] if transaction['category'] else '',
                payment_channel=transaction['payment_channel'],
            )

        # Supprimer les transactions supprimées
        Transaction.objects.filter(id__in=removed).delete()
        # for transaction in removed:
        #     Transaction.objects.filter(transaction_id=transaction['transaction_id']).delete()

        # Mettre à jour le curseur
        SyncCursor.objects.filter(bank=bank).update(cursor=cursor)
        # SyncCursor.objects.update(bank=bank, cursor=cursor)


# ---------------------------------------------------
    # def get_transaction(self, access_token, item_id):
    #     # Récupérer le cursor depuis la base de données
    #     sync_cursor = SyncCursor.objects.filter(bank__item_id=item_id).first()
    #     cursor = sync_cursor.cursor if sync_cursor else ""

    #     transactions = []
    #     has_more = True

    #     # Synchroniser les transactions
    #     while has_more:
    #         transaction_request = TransactionsSyncRequest(
    #             access_token=access_token,
    #             cursor=cursor if cursor else "",
    #         )
    #         transaction_response = plaid_config.client.transactions_sync(
    #             transaction_request)

    #         # Ajouter les transactions synchronisées
    #         transactions.extend(transaction_response["added"])

    #         # Mettre à jour le curseur
    #         cursor = transaction_response["next_cursor"]
    #         has_more = transaction_response["has_more"]

    #     # Formater les transactions
    #     formatted_transactions = [{
    #         'id': t['transaction_id'],
    #         'name': t['name'],
    #         'payment_channel': t['payment_channel'],
    #         'type': t['payment_channel'],
    #         'account_id': t['account_id'],
    #         'amount': t['amount'],
    #         'pending': t['pending'],
    #         'category': t['category'][0] if t['category'] else '',
    #         'date': t['date'],
    #         'image': t['logo_url'],
    #     } for t in transactions]

    #     return formatted_transactions