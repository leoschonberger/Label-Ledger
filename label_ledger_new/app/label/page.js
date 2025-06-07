"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import LabelPDF from "../components/LabelPDF";
import QRCode from "qrcode";

export default function Label() {
	const [newsData, setNewsData] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	const [qrCodes, setQrCodes] = useState([]);
	const router = useRouter();

	useEffect(() => {
		const fetchNews = async () => {
			try {
				const response = await fetch("/api/news", {
					method: "POST",
				});
				const data = await response.json();

				if (data.error) {
					throw new Error(data.error);
				}

				// Generate QR codes for each story with improved settings
				const codes = await Promise.all(
					data.stories.map(async (story) => {
						try {
							return await QRCode.toDataURL(story.url, {
								width: 200, // Increased size for better quality
								margin: 2, // Increased margin for better scanning
								errorCorrectionLevel: "H", // Highest error correction
								color: {
									dark: "#000000",
									light: "#ffffff",
								},
								scale: 4, // Higher scale for better quality
							});
						} catch (err) {
							console.error("Error generating QR code:", err);
							return null;
						}
					})
				);

				setQrCodes(codes);
				setNewsData({
					stories: data.stories,
					timestamp: new Date().toISOString(),
				});
			} catch (err) {
				setError(err.message);
			} finally {
				setLoading(false);
			}
		};

		fetchNews();
	}, []);

	if (loading) return <div>Loading...</div>;
	if (error) return <div>Error: {error}</div>;
	if (!newsData) return <div>No news data available</div>;

	return (
		<main className="flex min-h-screen flex-col items-center justify-center p-24">
			<div className="w-full max-w-4xl">
				<h1 className="text-3xl font-bold mb-8 text-center">
					Top News Headlines
				</h1>
				<div className="bg-white p-8 rounded-lg shadow-lg">
					<div className="space-y-6">
						{newsData.stories.map((story, index) => (
							<div
								key={index}
								className="border-b border-gray-200 pb-4 last:border-0 flex items-start gap-4"
							>
								<div className="flex-1">
									<h2 className="text-xl font-semibold mb-2">{story.title}</h2>
									<p className="text-gray-600 mb-2">{story.description}</p>
									<div className="text-sm text-gray-500">
										{new Date(story.published_at).toLocaleDateString()}
									</div>
								</div>
								<div className="flex-shrink-0 mt-2">
									{qrCodes[index] && (
										<img
											src={qrCodes[index]}
											alt="QR Code"
											className="w-24 h-24" // Increased size for better scanning
										/>
									)}
								</div>
							</div>
						))}
					</div>
				</div>
				<div className="mt-8 flex justify-center space-x-4">
					<button
						onClick={() => window.print()}
						className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
					>
						Print Label
					</button>
					<div className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded cursor-pointer">
						<LabelPDF newsData={newsData} />
					</div>
				</div>
			</div>
		</main>
	);
}
