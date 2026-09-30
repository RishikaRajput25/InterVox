import apiClient from "./client";
import { API_ENDPOINTS } from "./endpoints";

import type { Document } from "../../types/document";

export type DocumentUploadResponse = Document;

export async function uploadDocument(
  file: File
): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await apiClient.post<DocumentUploadResponse>(
    API_ENDPOINTS.documents.upload,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}