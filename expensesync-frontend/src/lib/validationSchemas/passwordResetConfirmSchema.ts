import * as z from "zod";

export const passwordResetConfirmSchema = z.object({
    uid: z.string().trim(),
    token: z.string().trim(),
    new_password: z
      .string()
      .min(8, { message: "Password must be at least 8 characters long" }),
    re_new_password: z.string().min(8, {
      message: "ConfirmPassword must be at least 8 characters long",
    }),
  })
  .refine((data) => data.new_password === data.re_new_password, {
    message: "Passwords do not match",
    path: ["re_new_password"],
});
