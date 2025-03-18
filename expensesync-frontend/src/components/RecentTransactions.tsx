import { RecentTransactionsProps } from "@/types";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Link from "next/link";

const RecentTransactions = ({ accounts, page }: RecentTransactionsProps) => {
  

  return (
    // <section className="recent-transactions">
    //   <header className="flex items-center justify-between">
    //     <h2 className="recent-transactions-label">Recent transactions</h2>
    //     <Link href={`/transaction-history/?id=`} className="view-all-btn">
    //       View all
    //     </Link>
    //   </header>
    //   <Tabs defaultValue="account" className="w-full">
    //     <TabsList className="recent-transactions-tablist">
    //       <TabsTrigger value="account">Account</TabsTrigger>
    //       <TabsTrigger value="password">Password</TabsTrigger>
    //     </TabsList>
    //     <TabsContent value="account">
    //       Make changes to your account here.
    //     </TabsContent>
    //     <TabsContent value="password">Change your password here.</TabsContent>
    //   </Tabs>
    // </section>
    <></>
  );
};
export default RecentTransactions;
