export type QueryValue = string | number | boolean | null | Record<string, unknown> | unknown[];

export interface QueryResponse {
  sql: string;
  columns: string[];
  rows: Record<string, QueryValue>[];
  row_count: number;
}

export interface ApiError {
  detail?: string;
}
