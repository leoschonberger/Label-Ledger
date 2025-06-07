"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState("");
	const router = useRouter();

	const handleGetNews = async () => {
		setIsLoading(true);
		setError("");

		try {
			const response = await fetch("/api/news", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({}),
			});

			const data = await response.json();
			console.log("API Response:", data);

			if (!response.ok) {
				throw new Error(data.error || "Failed to fetch news");
			}

			if (
				!data.stories ||
				!Array.isArray(data.stories) ||
				data.stories.length === 0
			) {
				throw new Error("No news stories found");
			}

			const newsData = {
				stories: data.stories,
				timestamp: new Date().toISOString(),
			};
			console.log("Storing news data:", newsData);
			localStorage.setItem("newsData", JSON.stringify(newsData));

			router.push("/label");
		} catch (err) {
			console.error("Error in handleGetNews:", err);
			setError(err.message);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<main className="flex min-h-screen flex-col items-center justify-center p-24">
			<div className="text-center">
				<h1 className="text-4xl font-bold mb-8">Label Ledger</h1>
				<p className="text-xl mb-8">
					Create your own mini-newspaper with current news topics
				</p>
				{error && <div className="text-red-500 text-sm mb-4">{error}</div>}
				<button
					onClick={handleGetNews}
					disabled={isLoading}
					className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
				>
					{isLoading ? "Loading..." : "Make my LabelLedger"}
				</button>
			</div>
		</main>
	);
}
