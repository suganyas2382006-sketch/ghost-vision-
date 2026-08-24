import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GhostVision Dashboard",
  description: "Real-time human segmentation and gesture recognition.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
