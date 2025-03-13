import { apiSlice } from "../../services/apiSlice";
import {
  ExchangePublicTokenResponse,
  PlaidLinkTokenResponse,
  ExchangeData,
  BankAccountResponse,
} from "@/types";

export const bankAccountApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getBankAccounts: builder.query<BankAccountResponse,void>({
      query: () => ({
        url: "/bank/get_accounts/",
        method: "GET",
      }),
      providesTags:["Account"]
    }),
    createPlaidLinkToken: builder.mutation<PlaidLinkTokenResponse, void>({
      query: () => ({
        url: "/bank/create-link-token/",
        method: "POST",
      }),
      invalidatesTags:["Account"]
    }),
    exchangePublicToken: builder.mutation<ExchangePublicTokenResponse,ExchangeData>({
      query: (data) => ({
        url: "/bank/exchange-public-token/",
        method: "POST",
        body: data
      }),
      invalidatesTags:["Account"]
    }),
  }),
});

export const {useCreatePlaidLinkTokenMutation, useExchangePublicTokenMutation, useGetBankAccountsQuery } = bankAccountApiSlice

