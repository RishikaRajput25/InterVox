export const API_ENDPOINTS = {
  documents: {
    upload: "/documents/upload",
    getById: (documentId: string) => `/documents/${documentId}`,
  },
} as const;