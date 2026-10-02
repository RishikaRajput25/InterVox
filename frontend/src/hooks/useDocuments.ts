import { useMutation, useQuery } from "@tanstack/react-query";

import {
  getDocumentById,
  uploadDocument,
  type DocumentUploadResponse,
} from "../services/api/documents";

export function useUploadDocument() {
  return useMutation<DocumentUploadResponse, Error, File>({
    mutationFn: uploadDocument,
  });
}

export function useDocumentStatus(documentId: string | null) {
  return useQuery({
    queryKey: ["document", documentId],
    queryFn: () => getDocumentById(documentId!),
    enabled: Boolean(documentId),
    refetchInterval: (query) => {
      const status = query.state.data?.status;

      if (status === "indexed" || status === "failed") {
        return false;
      }

      return 1000;
    },
  });
}