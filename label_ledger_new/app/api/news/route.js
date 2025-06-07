import { NextResponse } from "next/server";

export async function POST(request) {
	const apiKey = process.env.NEWS_API_KEY;

	if (!apiKey) {
		console.error("Missing NEWS_API_KEY");
		return NextResponse.json(
			{ error: "Missing NEWS_API_KEY" },
			{ status: 500 }
		);
	}

	// Get current date and date from 7 days ago
	const today = new Date();
	const oldest_story_date = new Date(today);
	oldest_story_date.setDate(today.getDate() - 7);

	// Format dates for API
	const fromDate = oldest_story_date.toISOString().split("T")[0];

	const url = `https://api.thenewsapi.com/v1/news/top?api_token=${apiKey}&language=en&limit=3&locale=us&published_after=${fromDate}`;
	console.log("Fetching news from URL:", url);

	try {
		const res = await fetch(url);
		if (!res.ok) {
			console.error("News API response not ok:", res.status, res.statusText);
			return NextResponse.json(
				{ error: "Failed to fetch news" },
				{ status: 500 }
			);
		}
		const response = await res.json();
		console.log("Raw API response:", response);
		console.log("Response type:", typeof response);
		console.log("Response keys:", Object.keys(response));

		// Check if we have data and it's in the expected format
		if (!response) {
			console.error("Invalid data format received:", response);
			return NextResponse.json(
				{ error: "Invalid data format received" },
				{ status: 500 }
			);
		}

		// Return the stories array from the data object
		const stories = response.data.map((story) => ({
			title: story.title,
			description: story.description,
			published_at: story.published_at,
			url: story.url,
			source: story.source,
		}));

		console.log("Processed stories:", stories);
		return NextResponse.json({ stories });
	} catch (error) {
		console.error("Error fetching news:", error);
		return NextResponse.json({ error: error.message }, { status: 500 });
	}
}
