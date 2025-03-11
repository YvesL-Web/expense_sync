import { apiSlice } from "../../services/apiSlice";
import {
  ExchangePublicTokenResponse,
  PlaidLinkTokenResponse,
  ExchangeData
} from "@/types";

export const bankAccountApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
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

export const {useCreatePlaidLinkTokenMutation, useExchangePublicTokenMutation} = bankAccountApiSlice

