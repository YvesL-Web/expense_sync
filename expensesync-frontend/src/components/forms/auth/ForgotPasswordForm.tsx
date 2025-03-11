"use client";

import CustomInput from "@/components/CustomInput";
import { Button } from "@/components/ui/button";
import { useResetPasswordRequestMutation } from "@/lib/redux/features/auth/authApiSlice";
import { passwordResetRequestSchema } from "@/lib/validationSchemas";
import extractErrorMessage from "@/utils/extractErrorMessage";
import { zodResolver } from "@hookform/resolvers/zod";
import { ChevronLeftCircle, Loader2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import * as z from "zod";

export default function ForgotPasswordForm() {
  const [resetPasswordRequest, { isLoading }] =
    useResetPasswordRequestMutation();
  const router = useRouter();
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(passwordResetRequestSchema),
    mode: "all",
    defaultValues: {
      email: "",
    },
  });
  const onSubmit = async (
    values: z.infer<typeof passwordResetRequestSchema>
  ) => {
    try {
      await resetPasswordRequest(values).unwrap();
      toast.success("Request sent, check your email for the reset link.");
      router.push("/login");
      reset();
    } catch (error) {
      const errorMessage = extractErrorMessage(error);
      toast.error(errorMessage || "An error occured");
    }
  };
  return (
    <div className="flex flex-col flex-1 lg:w-1/2 w-full">
      <div className="w-full max-w-md sm:pt-10 mx-auto mb-5">
        <Link
          href="/"
          className="inline-flex items-center text-md text-gray-500 transition-colors hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
          <ChevronLeftCircle />
          Back to dashboard
        </Link>
      </div>

      <div className="flex flex-col justify-center flex-1 w-full max-w-md mx-auto">
        <div>
          <div className="mb-5 sm:mb-8">
            <h1 className="mb-2 font-semibold  text-gray-800 text-3xl dark:text-white/90 sm:text-md">
              Forgot Your Password?
            </h1>
            <p className="text-md text-gray-500 dark:text-gray-400">
              Enter the email address linked to your account, and we&apos;ll
              send you a link to reset your password.
            </p>
          </div>
          <div>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-6">
                <CustomInput
                  type="email"
                  control={control}
                  errors={errors}
                  label="Email"
                  name="email"
                  placeholder="Enter your email address"
                />

                <div>
                  <Button
                    type="submit"
                    className="h4-semibold w-full text-white"
                    disabled={isLoading}>
                    {isLoading ? (
                      <Loader2 className="animate-spin" />
                    ) : (
                      "Request Password Reset."
                    )}
                  </Button>
                </div>
              </div>
            </form>

            <div className="mt-5">
              <p className="text-sm font-normal text-center text-gray-700 dark:text-gray-400 sm:text-start">
                Wait, I remember my password...
                <Link
                  href="/login"
                  className="hover:text-brand-600 dark:text-brand-400">
                  <span className="text-blue-500 hover:gradient-title">
                    {" "}
                    click here
                  </span>
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
