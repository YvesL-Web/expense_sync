import Image from "next/image";
import Link from "next/link";
import React from "react";

// import { countTransactionCategories } from "@/lib/utils";
// import Category from "./Category";
import BankCard from "./BankCard";
import {RightSidebarProps } from "@/types";

const RightSidebar = ({ user, banks }: RightSidebarProps) => {
  // const categories: CategoryCount[] = countTransactionCategories(transactions);
  return (
    <aside className="right-sidebar">
      <section className="flex flex-col pb-8">
        <div className="profile-banner" />
        <div className="profile">
          <div className="profile-img">
            <span className="text-5xl font-bold gradient-title">
              {user.first_name[0]}
            </span>
          </div>

          <div className="profile-details">
            <h1 className="profile-name">
              {user.first_name} {user.last_name}
            </h1>
            <p className="profile-email">{user.email}</p>
            {/* <p className="profile-email">{user.email}</p> */}
          </div>
        </div>
      </section>

      <section className="banks">
        <div className="flex w-full justify-between">
          <h2 className="header-2">My Banks</h2>
          <Link href="/" className="flex gap-2">
            <Image src="/icons/plus.svg" width={20} height={20} alt="plus" />
            <h2 className="text-14 font-semibold text-gray-600">Add Bank</h2>
          </Link>
        </div>

        {banks?.length > 0 && (
          <div className="relative flex flex-1 flex-col items-center justify-center gap-5">
            <div className="relative z-10">
              <BankCard
                // key={banks[0]}
                account={banks[0]}
                userName={`${user.first_name} ${user.last_name}`}
                showBalance={false}
              />
            </div>
            {banks[1] && (
              <div className="absolute right-0 top-8 z-0 w-[90%]">
                <BankCard
                  // key={banks[1]}
                  // account={banks[1] as unknown as BankAccount}
                  account={banks[1]}
                  userName={`${user.first_name} ${user.last_name}`}
                  showBalance={false}
                />
              </div>
            )}
          </div>
        )}

        {/* <div className="mt-10 flex flex-1 flex-col gap-6">
          <h2 className="header-2">Top categories</h2>

          <div className="space-y-5">
            {categories.map((category, index) => (
              <Category key={category.name} category={category} />
            ))}
          </div>
        </div> */}
      </section>
    </aside>
  );
};

export default RightSidebar;
