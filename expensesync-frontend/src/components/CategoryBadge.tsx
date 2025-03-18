import { cn } from "@/lib/utils"; 

export const transactionCategoryStyles = {
  "Food and Drink": {
    borderColor: "border-pink-600",
    backgroundColor: "bg-pink-500",
    textColor: "text-pink-700",
    chipBackgroundColor: "bg-inherit",
  },
  Payment: {
    borderColor: "border-green-600",
    backgroundColor: "bg-green-600",
    textColor: "text-green-700",
    chipBackgroundColor: "bg-inherit",
  },
  "Bank Fees": {
    borderColor: "border-green-600",
    backgroundColor: "bg-green-600",
    textColor: "text-green-700",
    chipBackgroundColor: "bg-inherit",
  },
  Transfer: {
    borderColor: "border-red-700",
    backgroundColor: "bg-red-700",
    textColor: "text-red-700",
    chipBackgroundColor: "bg-inherit",
  },
  Processing: {
    borderColor: "border-gray-300",
    backgroundColor: "bg-gray-500",
    textColor: "text-gray-700",
    chipBackgroundColor: "bg-gray-200",
  },
  Success: {
    borderColor: "border-green-500",
    backgroundColor: "bg-green-500",
    textColor: "text-green-700",
    chipBackgroundColor: "bg-green-100",
  },
  Travel: {
    borderColor: "border-blue-700",
    backgroundColor: "bg-blue-500",
    textColor: "text-blue-700",
    chipBackgroundColor: "bg-blue-100",
  },
  default: {
    borderColor: "border-blue-500",
    backgroundColor: "bg-blue-500",
    textColor: "text-blue-700",
    chipBackgroundColor: "bg-inherit",
  },
};

type CategoryBadgeProps = {
  category: keyof typeof transactionCategoryStyles | string;
};

const CategoryBadge = ({ category }: CategoryBadgeProps) => {
  const styles =
    transactionCategoryStyles[category as keyof typeof transactionCategoryStyles] ||
    transactionCategoryStyles.default;

  return (
    <div className={cn("category-badge flex items-center gap-2 p-2 rounded-xl", styles.borderColor, styles.chipBackgroundColor)}>
      <div className={cn("w-2 h-2 rounded-full", styles.backgroundColor)} />
      <p className={cn("text-[12px] font-medium", styles.textColor)}>{category}</p>
    </div>
  );
};

export default CategoryBadge;
