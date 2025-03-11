import { useLogoutMutation } from "@/lib/redux/features/auth/authApiSlice";
import { setLogout } from "@/lib/redux/features/auth/authSlice";
import { useAppDispatch } from "@/lib/redux/hooks/typedHook";
import extractErrorMessage from "@/utils/extractErrorMessage";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

const useLogout = () => {
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout().unwrap();
      dispatch(setLogout());
      router.push("/login");
      toast.success("Logged Out!");
    } catch (error) {
      const errorMessage = extractErrorMessage(error);
      toast.error(errorMessage || "An error occured.");
    }
  };

  return { handleLogout };
};
export default useLogout;
