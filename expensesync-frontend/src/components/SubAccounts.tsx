import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useGetAccountDetailsQuery } from "@/lib/redux/features/account/bankAccountApiSlice";
import { SubAccountTabItem } from "./SubAccountTabItem";
import { SubAccount } from "@/types";
import AccountInfo from "./AccountInfo";
import TransactionsTable from "./TransactionsTable";

interface subAccountProps {
  bank_account_id: string;
}
const SubAccounts = ({ bank_account_id }: subAccountProps) => {
  const { data, isLoading } = useGetAccountDetailsQuery(bank_account_id);
  if (isLoading) {
    return null;
  }
  console.log(data);
  
  return (
    <section className="recent-transactions">
      <Tabs defaultValue="account" className="w-full">
        <TabsList className="recent-transactions-tablist">
          {data && data.map((sub_account: SubAccount) => (
            <TabsTrigger
              key={sub_account.account_id}
              value={sub_account.account_id}>
              <SubAccountTabItem sub_account={sub_account} sub_account_id={sub_account.account_id} />
            </TabsTrigger>
          ))}
        </TabsList>
        {data && data.map((sub_account: SubAccount) => (
          <TabsContent key={sub_account.account_id} value={sub_account.account_id} className="space-y-4">
            <AccountInfo sub_account={sub_account} type="full" account_id={sub_account.account_id} />
            <TransactionsTable transactions={sub_account.transactions} />
          </TabsContent>
        ))}
        
      </Tabs>
    </section>
  );
};
export default SubAccounts;
