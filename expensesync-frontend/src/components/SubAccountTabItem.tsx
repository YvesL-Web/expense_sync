"use client";

import { useSearchParams, useRouter } from "next/navigation";

import { cn, formUrlQuery } from "@/lib/utils";
import { SubAccountItemProps } from "@/types";

export const SubAccountTabItem = ({ sub_account, sub_account_id }: SubAccountItemProps) => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const isActive = sub_account_id === sub_account?.account_id;

  const handleBankChange = () => {
    const newUrl = formUrlQuery({
      params: searchParams.toString(),
      key: "id",
      value: sub_account?.account_id,
    });
    router.push(newUrl, { scroll: false });
  };

  return (
    <div
      onClick={handleBankChange}
      className={cn(`banktab-item`, {
        " border-gray-950": isActive,
      })}
    >
      <p
        className={cn(`text-16 line-clamp-1 flex-1 font-medium text-gray-500`, {
          "text-RustEffect": isActive,
        })}
      >
        {sub_account.name}
      </p>
    </div>
  );
};
