import { create } from "zustand";

interface SelectedDocument {
  documentId: string;
  filename: string;
}

interface DocumentStore {
  selectedDocument: SelectedDocument | null;
  setSelectedDocument: (
    document: SelectedDocument
  ) => void;
  clearSelectedDocument: () => void;
}

export const useDocumentStore = create<DocumentStore>(
  (set) => ({
    selectedDocument: null,

    setSelectedDocument: (document) =>
      set({
        selectedDocument: document,
      }),

    clearSelectedDocument: () =>
      set({
        selectedDocument: null,
      }),
  })
);