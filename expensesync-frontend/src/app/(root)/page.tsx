"use client";

import HeaderBox from "@/components/HeaderBox";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import { useGetBankAccountsQuery } from "@/lib/redux/features/account/bankAccountApiSlice";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import { User } from "@/types";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Link from "next/link";
import { BankTabItem } from "@/components/BankTabItem";
import SubAccounts from "@/components/SubAccounts";

interface SearchParamProps {
  params: {
    // account_id: string;
    page: number | 1;
  };
}

const Page = ({ params: { page } }: SearchParamProps) => {
  const { data, isLoading } = useGetUserQuery();
  const { data: bankAccounts, isLoading: isBankaccountLoading } =
    useGetBankAccountsQuery();

  if (isLoading && isBankaccountLoading) {
    return null;
  }
  if (!bankAccounts) return null;

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
        {/* Test tab */}
        <section className="recent-transactions">
          <header className="flex items-center justify-between">
            <h2 className="recent-transactions-label">Recent transactions</h2>
            <Link href={`/transaction-history/?id=`} className="view-all-btn">
              View all
            </Link>
          </header>
          <Tabs className="w-full">
            <TabsList className="recent-transactions-tablist">
              {bankAccounts.accounts.map((account) => (
                <TabsTrigger
                  key={account.bank_account_id}
                  value={account.bank_account_id}>
                  <BankTabItem
                    account={account}
                    account_id={account.bank_account_id}
                  />
                </TabsTrigger>
              ))}
            </TabsList>
            {bankAccounts.accounts.map((account) => (
              <TabsContent key={account.bank_account_id} value={account.bank_account_id}>
                <SubAccounts bank_account_id={account.bank_account_id} />
              </TabsContent>
              ))}
          </Tabs>
        </section>
      </div>
      <RightSidebar
        user={data || ({} as User)}
        // transactions={account?.transactions}
        // banks={accountsData?.slice(0, 2)}
        transactions={[]}
        banks={bankAccounts.accounts}
      />
    </section>
  );
};
export default Page;
