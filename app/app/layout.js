import "./globals.css";

export const metadata = {
  title: "fit-docs-forge",
  description: "Preview UI scaffold for FIT documentation workflows.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
