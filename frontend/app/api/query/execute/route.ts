import { NextResponse } from "next/server";

export async function POST(request: Request) {
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ detail: "Request body must be valid JSON." }, { status: 400 });
  }

  const question = typeof payload === "object" && payload !== null && "question" in payload &&
    typeof payload.question === "string" ? payload.question.trim() : "";

  if (!question) {
    return NextResponse.json({ detail: "Query cannot be empty." }, { status: 422 });
  }

  const serviceUrl = process.env.QUERY_SERVICE_URL;
  if (!serviceUrl) {
    return NextResponse.json({ detail: "QUERY_SERVICE_URL is not configured." }, { status: 500 });
  }

  try {
    const response = await fetch(`${serviceUrl}/nl-query/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      cache: "no-store",
      signal: AbortSignal.timeout(35_000),
    });
    const body = await response.json().catch(() => ({ detail: "Query service returned an invalid response." }));
    return NextResponse.json(body, { status: response.status });
  } catch (error) {
    const timedOut = error instanceof Error && error.name === "TimeoutError";
    return NextResponse.json(
      { detail: timedOut ? "Query service timed out." : "Cannot connect to the query service." },
      { status: timedOut ? 504 : 502 },
    );
  }
}
