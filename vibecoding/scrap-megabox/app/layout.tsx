import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "메가박스 박스오피스 TOP 10",
  description: "메가박스 실시간 박스오피스 순위 1위~10위",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="bg-gray-950 text-white min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
