import type { Metadata } from "next";
import { Inter, IBM_Plex_Serif } from "next/font/google";
import "./globals.css";
import ReduxProvider from "@/lib/redux/provider";
import { Toaster } from "@/components/ui/sonner";
import PersistAuth from "@/utils/PersistAuth";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const ibmPlexSerif = IBM_Plex_Serif({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-ibm-plex-serif",
});

export const metadata: Metadata = {
  title: "ExpenseSync",
  description: "ExpenseSync is a modern money tracking platform for everyone.",
  icons: {
    icon: "/icons/temp-logo.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <ReduxProvider>
        <PersistAuth />
        <body className={`${inter.variable} ${ibmPlexSerif.variable}`}>
          <Toaster />
          {children}
        </body>
      </ReduxProvider>
      
    </html>
  );
}
