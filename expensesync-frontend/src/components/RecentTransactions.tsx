import { RecentTransactionsProps } from "@/types"
import Link from "next/link"

const RecentTransactions = ({accounts, page}: RecentTransactionsProps) => {
 
    console.log(accounts);
    
  
  return (
    <section className="recent-transactions">
      <header className="flex items-center justify-between">
        <h2 className="recent-transactions-label">Recent transactions</h2>
        <Link
          href={`/transaction-history/?id=`}
          className="view-all-btn"
        >
          View all
        </Link>
      </header>
      RecentTransactions
    </section>
  )
}
export default RecentTransactions