"use client"

import HeaderBox from "@/components/HeaderBox";
import RecentTransactions from "@/components/RecentTransactions";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import { useGetAccountDetailsQuery, useGetBankAccountsQuery } from "@/lib/redux/features/account/bankAccountApiSlice";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import { User } from "@/types";
import { string } from "zod";

interface SearchParamProps {
	params: {
		// account_id: string;
    page: number | 1;
	};
}

const Page = ({params: {page}}: SearchParamProps) => {
  const {data, isLoading} = useGetUserQuery() 
  const {data: bankAccounts , isLoading: isBankaccountLoading} = useGetBankAccountsQuery()
  const account_id = bankAccounts?.accounts[0].bank_account_id
  const {data: accountDetails} = useGetAccountDetailsQuery(account_id)


  if (isLoading && isBankaccountLoading) {
    return null;
  }
  if (!accountDetails) return null
  

  return (
    <section className="home">
      <div className="home-content">
        <header className="home-header">
          <HeaderBox
            type="greeting"
            title="Welcome"
            user={data?.first_name || "Guest"}
            subtext="Access and manage your account and transactions efficiently."
          />
          <TotalBalanceBox
            accounts={bankAccounts.accounts}
            total_banks={bankAccounts.total_banks}
            total_current_balance={bankAccounts.total_current_balance}
          />
        </header>
        {/* Recent Transactions */}
        <RecentTransactions accounts= {accountDetails} page={page} />
      </div>
      <RightSidebar 
        user={data || {} as User}
        // transactions={account?.transactions}
        // banks={accountsData?.slice(0, 2)}
        transactions={[]}
        banks={bankAccounts.accounts}
      />
    </section>
  );
};
export default Page;
