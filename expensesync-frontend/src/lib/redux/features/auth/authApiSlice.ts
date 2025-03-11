import { apiSlice } from "../../services/apiSlice";
import {
  ActivateUserData,
  RegisterUserData,
  RegisterUserResponse,
  ResetPasswordConfirmData,
  ResetPasswordData,
  SocialAuthArgs,
  SocialAuthResponse,
  UserResponse,
} from "@/types";

export const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getUser: builder.query<UserResponse, void>({
      query: () => ({
        url: "/auth/users/me/",
        method: "GET",
      }),
      providesTags: ["User"],
    }),
    socialAuthentication: builder.mutation<SocialAuthResponse, SocialAuthArgs>({
      query: ({ provider, state, code }) => ({
        url: `/auth/o/${provider}/?state=${encodeURIComponent(
          state
        )}&code=${encodeURIComponent(code)}`,
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }),
      invalidatesTags: ["User"],
    }),
    login: builder.mutation({
      query: ({ email, password }) => ({
        url: "/auth/jwt/create/",
        method: "POST",
        body: { email, password },
      }),
      invalidatesTags: ["User"],
    }),
    registerUser: builder.mutation<RegisterUserResponse, RegisterUserData>({
      query: (data) => ({
        url: "/auth/users/",
        method: "POST",
        body: data,
      }),
      invalidatesTags: ["User"],
    }),
    verify: builder.mutation({
      query: () => ({
        url: "/auth/jwt/verify/",
        method: "POST",
      }),
      invalidatesTags: ["User"],
    }),
    logout: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout/",
        method: "POST",
      }),
      invalidatesTags: ["User"],
    }),
    activateUser: builder.mutation<void, ActivateUserData>({
      query: (credentials) => ({
        url: "/auth/users/activation/",
        method: "POST",
        body: credentials,
      }),
      invalidatesTags: ["User"],
    }),
    resetPasswordRequest: builder.mutation<void, ResetPasswordData>({
      query: (data) => ({
        url: "/auth/users/reset_password/",
        method: "POST",
        body: data,
      }),
      invalidatesTags: ["User"],
    }),
    resetPasswordConfirm: builder.mutation<void, ResetPasswordConfirmData>({
      query: (data) => ({
        url: "/auth/users/reset_password_confirm/",
        method: "POST",
        body: data,
      }),
      invalidatesTags: ["User"],
    }),
    refreshJWT: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/jwt/refresh/",
        method: "POST",
      }),
      invalidatesTags: ["User"],
    }),
  }),
});

export const {
  useGetUserQuery,
  useSocialAuthenticationMutation,
  useLoginMutation,
  useRefreshJWTMutation,
  useRegisterUserMutation,
  useVerifyMutation,
  useLogoutMutation,
  useActivateUserMutation,
  useResetPasswordRequestMutation,
  useResetPasswordConfirmMutation,
} = authApiSlice;
