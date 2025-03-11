
import ForgotPasswordForm from "@/components/forms/auth/ForgotPasswordForm";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Forgot Password",
  description: "Request a new password.",
};

const PasswordReset = () => {
  return (
    <ForgotPasswordForm />
  )
}
export default PasswordReset