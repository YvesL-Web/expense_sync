/* eslint-disable no-unused-vars */

declare type SearchParamProps = {
  params: { [key: string]: string };
  searchParams: { [key: string]: string | string[] | undefined };
};

// ========================================

declare type SignUpParams = {
  first_name: string;
  last_name: string;
  address1: string;
  city: string;
  state: string;
  postalCode: string;
  dateOfBirth: string;
  ssn: string;
  email: string;
  password: string;
};

declare type LoginUser = {
  email: string;
  password: string;
};

declare type User = {
  // $id: string;
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  // userId: string;
  // dwollaCustomerUrl: string;
  // dwollaCustomerId: string;
  // name: string;
  // address1: string;
  // city: string;
  // state: string;
  // postalCode: string;
  // dateOfBirth: string;
  // ssn: string;
};

declare type NewUserParams = {
  userId: string;
  email: string;
  name: string;
  password: string;
};

declare type Account = {
  id: string;
  availableBalance: number;
  currentBalance: number;
  officialName: string;
  mask: string;
  institutionId: string;
  name: string;
  type: string;
  subtype: string;
  appwriteItemId: string;
  shareableId: string;
};

// declare type Transaction = {
//   id: string;
//   $id: string;
//   name: string;
//   paymentChannel: string;
//   type: string;
//   accountId: string;
//   amount: number;
//   pending: boolean;
//   category: string;
//   date: string;
//   image: string;
//   type: string;
//   $createdAt: string;
//   channel: string;
//   senderBankId: string;
//   receiverBankId: string;
// };

declare type Bank = {
  $id: string;
  accountId: string;
  bankId: string;
  accessToken: string;
  fundingSourceUrl: string;
  userId: string;
  shareableId: string;
};

declare type AccountTypes =
  | "depository"
  | "credit"
  | "loan "
  | "investment"
  | "other";

declare type Category = "Food and Drink" | "Travel" | "Transfer";

declare type CategoryCount = {
  name: string;
  count: number;
  totalCount: number;
};

declare type Receiver = {
  first_name: string;
  lastName: string;
};

declare type TransferParams = {
  sourceFundingSourceUrl: string;
  destinationFundingSourceUrl: string;
  amount: string;
};

declare type AddFundingSourceParams = {
  dwollaCustomerId: string;
  processorToken: string;
  bankName: string;
};

declare type NewDwollaCustomerParams = {
  first_name: string;
  lastName: string;
  email: string;
  type: string;
  address1: string;
  city: string;
  state: string;
  postalCode: string;
  dateOfBirth: string;
  ssn: string;
};

declare interface CreditCardProps {
  account: BankAccount;
  userName: string;
  showBalance?: boolean;
}

// declare interface BankInfoProps {
//   account: Account;
//   appwriteItemId?: string;
//   type: "full" | "card";
// }

declare interface HeaderBoxProps {
  type?: "title" | "greeting";
  title: string;
  subtext: string;
  user?: string;
}

declare interface MobileNavProps {
  user: User;
}

declare interface PageHeaderProps {
  topTitle: string;
  bottomTitle: string;
  topDescription: string;
  bottomDescription: string;
  connectBank?: boolean;
}

declare interface PaginationProps {
  page: number;
  totalPages: number;
}

declare interface PlaidLinkProps {
  isAuthenticated: boolean;
  variant?: "primary" | "ghost";
  // dwollaCustomerId?: string;
}

// declare type User = sdk.Models.Document & {
//   accountId: string;
//   email: string;
//   name: string;
//   items: string[];
//   accessToken: string;
//   image: string;
// };

declare interface AuthFormProps {
  type: "sign-in" | "sign-up";
}

declare interface BankDropdownProps {
  accounts: Account[];
  setValue?: UseFormSetValue<any>;
  otherStyles?: string;
}

// declare interface BankTabItemProps {
//   account: Account;
//   appwriteItemId?: string;
// }

declare interface TotalBalanceBoxProps {
  accounts: BankAccount[];
  totalBanks: number;
  totalCurrentBalance: number;
}

declare interface FooterProps {
  user: User;
  type?: "mobile" | "desktop";
}

declare interface RightSidebarProps {
  user: User;
  transactions: Transaction[];
  banks: BankAccount[];
}

declare interface SiderbarProps {
  user: User;
}

// declare interface RecentTransactionsProps {
//   accounts: Account[];
//   transactions: Transaction[];
//   appwriteItemId: string;
//   page: number;
// }

declare interface TransactionHistoryTableProps {
  transactions: Transaction[];
  page: number;
}

declare interface CategoryBadgeProps {
  category: string;
}

// declare interface TransactionTableProps {
//   transactions: Transaction[];
// }

declare interface CategoryProps {
  category: CategoryCount;
}

declare interface DoughnutChartProps {
  accounts: BankAccount[];
}

declare interface PaymentTransferFormProps {
  accounts: Account[];
}

// Actions
declare interface getAccountsProps {
  userId: string;
}

declare interface getAccountProps {
  appwriteItemId: string;
}

declare interface getInstitutionProps {
  institutionId: string;
}

declare interface getTransactionsProps {
  accessToken: string;
}

declare interface CreateFundingSourceOptions {
  customerId: string; // Dwolla Customer ID
  fundingSourceName: string; // Dwolla Funding Source Name
  plaidToken: string; // Plaid Account Processor Token
  _links: object; // Dwolla On Demand Authorization Link
}

declare interface CreateTransactionProps {
  name: string;
  amount: string;
  senderId: string;
  senderBankId: string;
  receiverId: string;
  receiverBankId: string;
  email: string;
}

declare interface getTransactionsByBankIdProps {
  bankId: string;
}

declare interface signInProps {
  email: string;
  password: string;
}

declare interface getUserInfoProps {
  userId: string;
}

declare interface exchangePublicTokenProps {
  publicToken: string;
  user: User;
}

declare interface createBankAccountProps {
  accessToken: string;
  userId: string;
  accountId: string;
  bankId: string;
  fundingSourceUrl: string;
  shareableId: string;
}

declare interface getBanksProps {
  userId: string;
}

declare interface getBankProps {
  documentId: string;
}

declare interface getBankByAccountIdProps {
  accountId: string;
}

// ========== User =======
export interface UserResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface SocialAuthResponse {
  success: string;
  user: User;
}

export interface SocialAuthArgs {
  provider: string;
  state: string;
  code: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface ResetPasswordConfirmData extends ActivateUserData {
  new_password: string;
  re_new_password: string;
}

export interface RegisterUserResponse {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface RegisterUserData {
  first_name: string;
  last_name: string;
  password: string;
  re_password: string;
}

export interface ActivateUserData {
  uid: string;
  token: string;
}

export interface PlaidLinkTokenResponse {
  link_token: string;
  expiration: string;
  request_id: string;
}

export interface ExchangePublicTokenResponse {
  detail: string;
}

export interface ExchangeData {
  public_token: string;
  metadata: {
    institution: {
      name: string | "";
      institution_id: string | "";
    };
  };
}

export interface BankAccount {
  bank_account_id: string;
  institution_id: string;
  available_balance: number;
  institution_name: string;
}

export interface BankAccountResponse {
  accounts: BankAccount[];
  total_banks: number;
  total_current_balance: number;
}

export interface Transaction {
  transaction_id: string;
  account_id: string;
  name: string;
  amount: number;
  date: Date;
  payment_channel: string;
  pending: boolean;
  category: string;
  image: string;
}

declare interface TransactionTableProps {
  transactions: Transaction[];
}

export interface SubAccount {
  account_id: string;
  institution_id: string;
  current_balance: number;
  name: string;
  official_name: string;
  type: string;
  subtype: string;
  transactions: Transaction[];
}

export interface AcccountDetailsResponse {
  data: SubAccount[];
}

declare interface RecentTransactionsProps {
  accounts: AcccountDetailsResponse;
  page: number;
}

declare interface BankTabItemProps {
  account: BankAccount;
  account_id: string;
}
declare interface SubAccountItemProps {
  sub_account: SubAccount;
  sub_account_id: string;
}

declare interface AccountInfoProps {
  sub_account: SubAccount;
  account_id?: string;
  type: "full" | "card";
}