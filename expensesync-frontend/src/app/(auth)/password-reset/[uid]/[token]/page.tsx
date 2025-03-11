
import PasswordResetForm from "@/components/forms/auth/PasswordResetForm";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Reset Password page",
  description: "Request a new password.",
};

const PasswordReset = () => {
  return (
    <PasswordResetForm />
  )
}
export default PasswordReset