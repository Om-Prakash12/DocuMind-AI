export interface Document {
  filename: string;
  total_chunks: number;
  chunks: (string | number)[];
}

export interface DocumentListResponse {
  total_documents: number;
  documents: Document[];
}