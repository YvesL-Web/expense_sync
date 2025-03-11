"use client"

import HeaderBox from "@/components/HeaderBox";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import { User } from "@/types";

const Page = () => {
  const {data, isLoading} = useGetUserQuery() 
  if (isLoading) {
    return null;
  }
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
            accounts={[]}
            totalBanks={1}
            totalCurrentBalance={5000.5}
          />
        </header>
        {/* Recent Transactions */}
      </div>
      <RightSidebar 
        user={data || {} as User}
        // transactions={account?.transactions}
        // banks={accountsData?.slice(0, 2)}
        transactions={[]}
        banks={[]}
      />
    </section>
  );
};
export default Page;
