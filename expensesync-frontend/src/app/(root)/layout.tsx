"use client"
import MobileNav from "@/components/MobileNav";
import Sidebar from "@/components/Sidebar";
// import useGetLoggedinUser from "@/hooks/useGetLoggedinUser";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import Image from "next/image";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const {data, isLoading} = useGetUserQuery() 
    if (isLoading) {
      return null;
    }
  if (!data) {
    return null;
  }

    // next option for optimization
  // const user = useGetLoggedinUser()

  return (
    <main className="flex h-screen w-full font-inter">
      <Sidebar user={data} />
      <div className="flex size-full flex-col">
        <div className="root-layout">
          <Image src="/icons/temp-logo.svg" width={30} height={30} alt="logo" />
          <div>
            <MobileNav user={data} />
          </div>
        </div>
        {children}
      </div>
    </main>
  );
 
}

 // return (
  //   <main className="flex h-screen w-full font-inter">
  //     {user && <Sidebar user={user} />}
  //     <div className="flex size-full flex-col">
  //       <div className="root-layout">
  //         <Image src="/icons/temp-logo.svg" width={30} height={30} alt="logo" />
  //         <div>
  //           {user && <MobileNav user={user} />}
  //         </div>
  //       </div>
  //       {children}
  //     </div>
  //   </main>
  // );