"use client";

import {
	Document,
	Page,
	Text,
	View,
	StyleSheet,
	PDFDownloadLink,
	Image,
} from "@react-pdf/renderer";
import QRCode from "qrcode";
import { useState, useEffect } from "react";

// Create styles
const styles = StyleSheet.create({
	page: {
		padding: 20,
		width: "4in",
		height: "6in",
	},
	header: {
		marginBottom: 10,
		borderBottom: "1 solid #000",
		paddingBottom: 5,
	},
	title: {
		fontSize: 18,
		marginBottom: 2,
		textAlign: "center",
	},
	date: {
		fontSize: 10,
		textAlign: "center",
		color: "#666",
	},
	story: {
		marginBottom: 8,
		flexDirection: "row",
	},
	storyContent: {
		flex: 1,
		marginRight: 10,
	},
	headline: {
		fontSize: 11,
		fontWeight: "bold",
		marginBottom: 2,
	},
	summary: {
		fontSize: 8,
		color: "#333",
		marginBottom: 2,
	},
	timestamp: {
		fontSize: 6,
		color: "#666",
	},
	downloadButton: {
		fontSize: 10,
		color: "#fff",
	},
	qrcode: {
		width: 80,
		height: 80,
	},
});

// Create Document Component
const LabelDocument = ({ newsData, qrCodes }) => (
	<Document>
		<Page size={[288, 432]} style={styles.page}>
			{" "}
			{/* 4x6 inches in points (72 points per inch) */}
			<View style={styles.header}>
				<Text style={styles.title}>Top News Headlines</Text>
				<Text style={styles.date}>
					{new Date(newsData.timestamp).toLocaleDateString("en-US", {
						weekday: "long",
						year: "numeric",
						month: "long",
						day: "numeric",
					})}
				</Text>
			</View>
			{newsData.stories.map((story, index) => (
				<View key={index} style={styles.story}>
					<View style={styles.storyContent}>
						<Text style={styles.headline}>{story.title}</Text>
						<Text style={styles.summary}>{story.description}</Text>
						<Text style={styles.timestamp}>
							{new Date(story.published_at).toLocaleDateString()}
						</Text>
					</View>
					{qrCodes[index] && (
						<Image src={qrCodes[index]} style={styles.qrcode} />
					)}
				</View>
			))}
		</Page>
	</Document>
);

export default function LabelPDF({ newsData }) {
	const [qrCodes, setQrCodes] = useState([]);

	useEffect(() => {
		// Generate QR codes for each story with improved settings
		const generateQRCodes = async () => {
			const codes = await Promise.all(
				newsData.stories.map(async (story) => {
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
		};

		generateQRCodes();
	}, [newsData]);

	return (
		<PDFDownloadLink
			document={<LabelDocument newsData={newsData} qrCodes={qrCodes} />}
			fileName={`top-news-${new Date().toISOString().split("T")[0]}.pdf`}
		>
			{({ blob, url, loading, error }) => (
				<Text style={styles.downloadButton}>
					{loading ? "Generating PDF..." : "Download PDF"}
				</Text>
			)}
		</PDFDownloadLink>
	);
}
