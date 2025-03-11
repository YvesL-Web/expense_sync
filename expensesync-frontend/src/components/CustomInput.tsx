import React, { useState } from "react";
import {
  Controller,
  Control,
  FieldErrors,
  FieldValues,
  Path,
} from "react-hook-form";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { EyeClosed, EyeIcon } from "lucide-react";

// Définition des props du composant
interface CustomInputProps<T extends FieldValues> {
  name: Path<T>;
  label: string;
  placeholder?: string; // Placeholder du champ (optionnel)
  type: React.HTMLInputTypeAttribute;
  control: Control<T>;
  errors: FieldErrors<T>;
}

const CustomInput = <T extends FieldValues>({
  name,
  label,
  placeholder,
  type,
  control,
  errors,
}: CustomInputProps<T>) => {
    const [showPassword, setShowPassword] = useState(false);
  return (
    <div className="form-item">
      {/* Label du champ */}
      <Label className="form-label" htmlFor={name}>
        {label}
      </Label>

      {/* Champ de saisie */}
      <div className="flex w-full flex-col">
        {type === "password" ? (
          <Controller
            name={name}
            control={control}
            render={({ field }) => (
              <div className="relative">
                <Input
                  {...field}
                  id={name}
                  type={showPassword ? "text" : "password"}
                  placeholder={placeholder}
                  className={errors[name] ? "border-red-500" : ""}
                />
                <span
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute z-30 -translate-y-1/2 cursor-pointer right-4 top-1/2">
                  {showPassword ? (
                    <EyeIcon className="text-black dark:text-white" />
                  ) : (
                    <EyeClosed className="text-black dark:text-white" />
                  )}
                </span>
              </div>
            )}
          />
        ) : (
          <Controller
            name={name}
            control={control}
            render={({ field }) => (
              <Input
                {...field}
                id={name}
                type={type}
                placeholder={placeholder}
                className={errors[name] ? "border-red-500" : ""}
              />
            )}
          />
        )}

        {/* Affichage des erreurs de validation */}
        {errors[name] && (
          <p className="form-message mt-2">
            {typeof errors[name]?.message === "string" && errors[name]?.message}
            {/* {typeof formState.errors[name]?.message === "string" && formState.errors[name]?.message} */}
          </p>
        )}
      </div>
    </div>
  );
};

export default CustomInput;
