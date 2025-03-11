"use client";

import * as z from "zod";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { registerUserSchema } from "@/lib/validationSchemas";
import { useRouter } from "next/navigation";
import CustomInput from "@/components/CustomInput";
import { Loader2 } from "lucide-react";
import { useRegisterUserMutation } from "@/lib/redux/features/auth/authApiSlice";
import { useAppSelector } from "@/lib/redux/hooks/typedHook";
import { toast } from "sonner";
import extractErrorMessage from "@/utils/extractErrorMessage";


const RegisterForm = () => {
  const router = useRouter();
  const [registerUser, { isLoading }] = useRegisterUserMutation();
  const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);

  const {
    handleSubmit,
    reset,
    control,
    formState: { errors },
  } = useForm<z.infer<typeof registerUserSchema>>({
    resolver: zodResolver(registerUserSchema),
    mode: "all",
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      re_password: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof registerUserSchema>) => {
    try {
      await registerUser(data).unwrap();
      toast.success(
        "An email with an activation link has been sent to your email address. Please check your email and activate your account. "
      );
      router.push("/login");
      reset();
    } catch (error: any) {
      const errorMessage = extractErrorMessage(error);
      toast.error(errorMessage);
    }
  };

  return (
    <section className="auth-form">
      <header className="flex flex-col gap-5 md:gap-8">
        <Link href="/" className="cursor-pointer flex items-center gap-1 px-4">
          <Image
            src="/icons/temp-logo.svg"
            width={100}
            height={100}
            alt="Horizon logo"
          />
          <h1 className="text-26 font-ibm-plex-serif font-bold text-black-1">
            ExpenseSync
          </h1>
        </Link>
        <div className="flex flex-col gap-1 md:gap-3">
          <h1 className="text-24 lg:text-36 font-semibold text-gray-900">
            Sign Up
            <p className="text-16 font-normal text-gray-600">
              {isAuthenticated
                ? "Link your account to get started"
                : "Please enter your details"}
            </p>
          </h1>
        </div>
      </header>
      {isAuthenticated ? (
        <div className="flex flex-col gap-4">{/* PlaidLink */}</div>
      ) : (
        <>
          <form className="space-y-8" onSubmit={handleSubmit(onSubmit)}>
            <CustomInput
              control={control}
              errors={errors}
              label="Firstname"
              name="first_name"
              type="text"
              placeholder="Enter your firstname"
            />
            <CustomInput
              control={control}
              errors={errors}
              label="Lastname"
              name="last_name"
              type="text"
              placeholder="Enter your lastname"
            />
            <CustomInput
              control={control}
              errors={errors}
              label="Email"
              name="email"
              type="email"
              placeholder="Enter your email"
            />

            <CustomInput
              control={control}
              errors={errors}
              label="Password"
              name="password"
              type="password"
              placeholder="Enter your password"
            />
            <CustomInput
              control={control}
              errors={errors}
              label="Confirm password"
              name="re_password"
              type="password"
              placeholder="Confirm your password"
            />
            <div className="flex flex-col gap-4">
              <Button
                type="submit"
                className="w-full form-btn"
                disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 size={20} className="animate-spin" /> &nbsp;
                    Loading....
                  </>
                ) : (
                  "Sign Up"
                )}
              </Button>
            </div>
          </form>
          <footer className="flex justify-center gap-1">
            <p className="text-14 font-normal text-gray-600">
              Already have an account?
            </p>
            <Link href="/login" className="form-link hover:gradient-title">
              Sign in
            </Link>
          </footer>
        </>
      )}
    </section>
  );
};
export default RegisterForm;
