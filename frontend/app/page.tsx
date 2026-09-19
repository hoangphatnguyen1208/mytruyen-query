"use client";

import { FormEvent, useState } from "react";
import type { ApiError, QueryResponse, QueryValue } from "@/types/query";

const EXAMPLE_QUERY = "Tìm 10 quyển sách có lượt xem cao nhất";

function formatValue(value: QueryValue | undefined): string {
  if (value === null || value === undefined) return "NULL";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

export default function Home() {
  const [question, setQuestion] = useState(EXAMPLE_QUERY);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runQuery(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = question.trim();
    if (!value || loading) return;
    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/query/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: value }),
      });
      const body = (await response.json()) as QueryResponse | ApiError;
      if (!response.ok) {
        throw new Error("detail" in body && body.detail ? body.detail : "The query could not be executed.");
      }
      setResult(body as QueryResponse);
    } catch (caught) {
      setResult(null);
      setError(caught instanceof Error ? caught.message : "Unexpected error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f5f7f9] text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-[1500px] items-center justify-between px-5 py-4 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-lg bg-slate-900 font-mono text-sm font-bold text-white">SQL</div>
            <div>
              <h1 className="text-base font-semibold leading-tight">MyTruyen Query</h1>
              <p className="text-xs text-slate-500">Natural language database console</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs font-medium text-slate-600">
            <span className="h-2 w-2 rounded-full bg-emerald-500" /> Backend :8000
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1500px] gap-5 p-5 lg:p-8">
        <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-3">
            <div>
              <h2 className="text-sm font-semibold">Query editor</h2>
              <p className="mt-0.5 text-xs text-slate-500">Describe the data you want to retrieve.</p>
            </div>
            <span className="rounded-md bg-slate-100 px-2 py-1 font-mono text-[11px] text-slate-500">Natural language</span>
          </div>
          <form onSubmit={runQuery}>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if ((event.ctrlKey || event.metaKey) && event.key === "Enter") event.currentTarget.form?.requestSubmit();
              }}
              className="min-h-40 w-full resize-y border-0 bg-[#fbfcfd] p-5 font-mono text-sm leading-6 outline-none placeholder:text-slate-400"
              placeholder="Example: Find the 10 most viewed books"
              spellCheck={false}
            />
            <div className="flex items-center justify-between border-t border-slate-200 px-5 py-3">
              <span className="text-xs text-slate-400">Ctrl + Enter to run</span>
              <button type="submit" disabled={loading || !question.trim()} className="inline-flex min-w-28 items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50">
                {loading ? <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" /> : <span className="text-[10px]">▶</span>}
                {loading ? "Running" : "Run query"}
              </button>
            </div>
          </form>
        </section>

        {error && <div role="alert" className="rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700"><span className="font-semibold">Query failed:</span> {error}</div>}

        <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-5 py-3"><h2 className="text-sm font-semibold">Generated SQL</h2></div>
          <pre className="min-h-28 overflow-x-auto whitespace-pre-wrap bg-[#101722] p-5 font-mono text-[13px] leading-6 text-slate-200">
            {result?.sql ?? "-- Run a query to view the generated SQL"}
          </pre>
        </section>

        <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-3">
            <h2 className="text-sm font-semibold">Results</h2>
            <span className="text-xs text-slate-500">{result ? `${result.row_count ?? result.rows.length} rows` : "No results"}</span>
          </div>
          {!result ? (
            <div className="grid min-h-52 place-items-center p-8 text-center"><div><div className="mx-auto mb-3 grid h-10 w-10 place-items-center rounded-lg bg-slate-100 font-mono text-slate-400">▦</div><p className="text-sm font-medium text-slate-600">Results will appear here</p><p className="mt-1 text-xs text-slate-400">Execute a query to retrieve data.</p></div></div>
          ) : result.rows.length === 0 ? (
            <div className="grid min-h-40 place-items-center text-sm text-slate-500">The query returned no rows.</div>
          ) : (
            <div className="max-h-[520px] overflow-auto">
              <table className="w-full min-w-max border-collapse text-left text-sm">
                <thead className="sticky top-0 z-10 bg-slate-50"><tr><th className="border-b border-r border-slate-200 px-4 py-3 text-xs font-semibold text-slate-500">#</th>{result.columns.map((column) => <th key={column} className="border-b border-r border-slate-200 px-4 py-3 font-mono text-xs font-semibold text-slate-600 last:border-r-0">{column}</th>)}</tr></thead>
                <tbody>{result.rows.map((row, rowIndex) => <tr key={rowIndex} className="hover:bg-slate-50/70"><td className="border-b border-r border-slate-100 px-4 py-3 font-mono text-xs text-slate-400">{rowIndex + 1}</td>{result.columns.map((column) => <td key={`${rowIndex}-${column}`} className="max-w-[420px] border-b border-r border-slate-100 px-4 py-3 font-mono text-xs text-slate-700 last:border-r-0"><span className="block overflow-hidden text-ellipsis whitespace-nowrap" title={formatValue(row[column])}>{formatValue(row[column])}</span></td>)}</tr>)}</tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
