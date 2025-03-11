"use client";

import CustomInput from "@/components/CustomInput";
import { Button } from "@/components/ui/button";
import { useResetPasswordConfirmMutation } from "@/lib/redux/features/auth/authApiSlice";
import { passwordResetConfirmSchema } from "@/lib/validationSchemas";
import extractErrorMessage from "@/utils/extractErrorMessage";
import { zodResolver } from "@hookform/resolvers/zod";
import { ChevronLeftCircle, Loader2 } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import * as z from "zod";

export default function PasswordResetForm() {
  const router = useRouter();
  const { uid, token } = useParams<{ uid: string; token: string }>();

  const [resetPasswordConfirm, { isLoading }] =
    useResetPasswordConfirmMutation();
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(passwordResetConfirmSchema),
    mode: "all",
    defaultValues: {
      uid: uid as string,
      token: token as string,
      new_password: "",
      re_new_password: "",
    },
  });

  const onSubmit = async (
    values: z.infer<typeof passwordResetConfirmSchema>
  ) => {
    try {
      await resetPasswordConfirm({
        ...values,
        uid: uid as string,
        token: token as string,
      }).unwrap();
      router.push("/login");
      toast.success("Your password has been reset successfully.");
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
              Create A New Password
            </h1>
            <p className="text-md text-gray-500 dark:text-gray-400">
              Enter a new password
            </p>
          </div>
          <div>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-6">
                <div>
                  <CustomInput
                    type="password"
                    control={control}
                    errors={errors}
                    label="New password"
                    name="new_password"
                  />
                </div>
                <div>
                  <CustomInput
                    type="password"
                    control={control}
                    errors={errors}
                    label="Comfirm new password"
                    name="re_new_password"
                  />
                </div>

                <div>
                  <Button
                    type="submit"
                    className="h4-semibold w-full text-white"
                    disabled={isLoading}>
                    {isLoading ? (
                      <Loader2 className="animate-spin" />
                    ) : (
                      "Confirm"
                    )}
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
