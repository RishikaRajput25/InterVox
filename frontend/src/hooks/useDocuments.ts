import { useMutation } from "@tanstack/react-query";

import {
  uploadDocument,
  type DocumentUploadResponse,
} from "../services/api/documents";

export function useUploadDocument() {
  return useMutation<DocumentUploadResponse, Error, File>({
    mutationFn: uploadDocument,
  });
}