import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BrahmX AI",
  description: "Smart AI chatbot powered by NLP and Transformers",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="app-body">
        {children}
      </body>
    </html>
  );
}