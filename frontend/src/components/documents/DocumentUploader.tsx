
// import {
//   useEffect,
//   useRef,
//   useState,
// } from "react";

// import {
//   useDocumentStatus,
//   useUploadDocument,
// } from "../../hooks/useDocuments";

// import { useDocumentStore } from "../../stores/documentStore";

// function DocumentUploader() {
//   const inputRef = useRef<HTMLInputElement>(null);

//   const uploadMutation = useUploadDocument();

//   const setSelectedDocument =
//     useDocumentStore(
//       (state) => state.setSelectedDocument
//     );

//   const [selectedFile, setSelectedFile] =
//     useState<File | null>(null);

//   const [documentId, setDocumentId] =
//     useState<string | null>(null);

//   const documentStatus =
//     useDocumentStatus(documentId);

//   const handleFileSelect = (file: File) => {
//     setSelectedFile(file);
//     setDocumentId(null);
//     uploadMutation.reset();
//   };

//   const handleUpload = async () => {
//     if (!selectedFile) {
//       return;
//     }

//     try {
//       const document =
//         await uploadMutation.mutateAsync(
//           selectedFile
//         );

//       setDocumentId(
//         document.document_id
//       );
//     } catch {
//       // Error is already available
//       // through uploadMutation.error
//     }
//   };

//   const status =
//     documentStatus.data?.status;

//   useEffect(() => {
//     if (
//       status !== "indexed" ||
//       !documentStatus.data
//     ) {
//       return;
//     }

//     setSelectedDocument({
//       documentId:
//         documentStatus.data.document_id,
//       filename:
//         documentStatus.data.original_filename,
//     });
//   }, [
//     status,
//     documentStatus.data,
//     setSelectedDocument,
//   ]);

//   return (
//     <div className="w-full max-w-xl">
//       <div
//         onClick={() =>
//           inputRef.current?.click()
//         }
//         className="cursor-pointer rounded-2xl border border-dashed border-slate-700 bg-slate-900/40 p-10 text-center transition hover:border-slate-500 hover:bg-slate-900/70"
//       >
//         <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-800 text-slate-300">
//           ↑
//         </div>

//         <h2 className="mt-5 text-lg font-medium text-white">
//           Upload your research document
//         </h2>

//         <p className="mt-2 text-sm text-slate-500">
//           PDF, DOCX or TXT files up to 10 MB
//         </p>

//         <input
//           ref={inputRef}
//           type="file"
//           accept=".pdf,.docx,.txt"
//           className="hidden"
//           onChange={(event) => {
//             const file =
//               event.target.files?.[0];

//             if (file) {
//               handleFileSelect(file);
//             }
//           }}
//         />
//       </div>

//       {selectedFile && (
//         <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/70 p-4">
//           <div className="flex items-center justify-between gap-4">
//             <div className="min-w-0">
//               <p className="truncate text-sm font-medium text-slate-200">
//                 {selectedFile.name}
//               </p>

//               <p className="mt-1 text-xs text-slate-500">
//                 {(
//                   selectedFile.size /
//                   1024 /
//                   1024
//                 ).toFixed(2)}{" "}
//                 MB
//               </p>
//             </div>

//             <button
//               type="button"
//               onClick={handleUpload}
//               disabled={
//                 uploadMutation.isPending ||
//                 documentStatus.isFetching
//               }
//               className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
//             >
//               {uploadMutation.isPending
//                 ? "Uploading..."
//                 : status === "processing"
//                   ? "Processing..."
//                   : status === "indexed"
//                     ? "Ready"
//                     : "Upload"}
//             </button>
//           </div>
//         </div>
//       )}

//       {uploadMutation.isPending && (
//         <div className="mt-4 rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-4 text-sm text-indigo-400">
//           Uploading document...
//         </div>
//       )}

//       {status === "processing" && (
//         <div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 text-sm text-amber-400">
//           Processing and indexing your document...
//         </div>
//       )}

//       {status === "indexed" && (
//         <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 text-sm text-emerald-400">
//           Document is ready. You can now ask questions about it.
//         </div>
//       )}

//       {status === "failed" && (
//         <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
//           {documentStatus.data?.processing_error ||
//             "Document processing failed."}
//         </div>
//       )}

//       {uploadMutation.isError && (
//         <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
//           {uploadMutation.error.message}
//         </div>
//       )}
//     </div>
//   );
// }

// export default DocumentUploader;



import {
  useEffect,
  useRef,
  useState,
} from "react";
import { useNavigate } from "react-router-dom";

import {
  useDocumentStatus,
  useUploadDocument,
} from "../../hooks/useDocuments";

import { useDocumentStore } from "../../stores/documentStore";

function DocumentUploader() {
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const uploadMutation = useUploadDocument();

  const setSelectedDocument =
    useDocumentStore(
      (state) => state.setSelectedDocument
    );

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [documentId, setDocumentId] =
    useState<string | null>(null);

  const documentStatus =
    useDocumentStatus(documentId);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setDocumentId(null);
    uploadMutation.reset();
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      return;
    }

    try {
      const document =
        await uploadMutation.mutateAsync(
          selectedFile
        );

      setDocumentId(
        document.document_id
      );
    } catch {
      // Error is available through uploadMutation.error
    }
  };

  const status =
    documentStatus.data?.status;

  useEffect(() => {
    if (
      status !== "indexed" ||
      !documentStatus.data
    ) {
      return;
    }

    setSelectedDocument({
      documentId:
        documentStatus.data.document_id,
      filename:
        documentStatus.data.original_filename,
    });

    // Automatically move to Voice Assistant.
    navigate("/");
  }, [
    status,
    documentStatus.data,
    setSelectedDocument,
    navigate,
  ]);

  return (
    <div className="w-full max-w-xl">
      <div
        onClick={() =>
          inputRef.current?.click()
        }
        className="cursor-pointer rounded-2xl border border-dashed border-slate-700 bg-slate-900/40 p-10 text-center transition hover:border-slate-500 hover:bg-slate-900/70"
      >
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-800 text-slate-300">
          ↑
        </div>

        <h2 className="mt-5 text-lg font-medium text-white">
          Upload your research document
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          PDF, DOCX or TXT files up to 10 MB
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={(event) => {
            const file =
              event.target.files?.[0];

            if (file) {
              handleFileSelect(file);
            }
          }}
        />
      </div>

      {selectedFile && (
        <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="flex items-center justify-between gap-4">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-slate-200">
                {selectedFile.name}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                {(
                  selectedFile.size /
                  1024 /
                  1024
                ).toFixed(2)}{" "}
                MB
              </p>
            </div>

            <button
              type="button"
              onClick={handleUpload}
              disabled={
                uploadMutation.isPending ||
                documentStatus.isFetching
              }
              className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {uploadMutation.isPending
                ? "Uploading..."
                : status === "processing"
                  ? "Processing..."
                  : status === "indexed"
                    ? "Ready"
                    : "Upload"}
            </button>
          </div>
        </div>
      )}

      {uploadMutation.isPending && (
        <div className="mt-4 rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-4 text-sm text-indigo-400">
          Uploading document...
        </div>
      )}

      {status === "processing" && (
        <div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 text-sm text-amber-400">
          Processing and indexing your document...
        </div>
      )}

      {status === "indexed" && (
        <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 text-sm text-emerald-400">
          Document is ready. Opening Voice Assistant...
        </div>
      )}

      {status === "failed" && (
        <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
          {documentStatus.data?.processing_error ||
            "Document processing failed."}
        </div>
      )}

      {uploadMutation.isError && (
        <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
          {uploadMutation.error.message}
        </div>
      )}
    </div>
  );
}

export default DocumentUploader;