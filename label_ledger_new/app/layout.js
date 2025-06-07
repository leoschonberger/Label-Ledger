import "./globals.css";

export const metadata = {
	title: "Label Ledger",
	description: "Create a downloadable label with current news topics",
};

export default function RootLayout({ children }) {
	return (
		<html lang="en">
			<body className="min-h-screen bg-gray-50">{children}</body>
		</html>
	);
}
