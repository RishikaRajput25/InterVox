export interface Document {
  document_id: string;
  original_filename: string;
  stored_filename: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
  status: "uploaded" | "processing" | "processed" | "indexed" | "failed";
  processing_error: string | null;
}