import { useState } from "react";
import type { FormEvent } from "react";

import { useAskQuestion } from "../../hooks/useQuestions";

interface QuestionPanelProps {
  documentId: string | null;
  documentName?: string;
}

function QuestionPanel({
  documentId,
  documentName,
}: QuestionPanelProps) {
  const [question, setQuestion] = useState("");

  const askQuestionMutation = useAskQuestion();

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!documentId || !question.trim()) {
      return;
    }

    await askQuestionMutation.mutateAsync({
      question: question.trim(),
      document_id: documentId,
    });
  };

  const result = askQuestionMutation.data;

  return (
    <div className="w-full max-w-3xl">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl shadow-black/10">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-indigo-400">
            Research Assistant
          </p>

          <h2 className="mt-2 text-xl font-semibold text-white">
            Ask about your document
          </h2>

          {documentName && (
            <p className="mt-1 text-sm text-slate-500">
              Currently selected: {documentName}
            </p>
          )}
        </div>

        <form
          onSubmit={handleSubmit}
          className="mt-6"
        >
          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder={
              documentId
                ? "Ask a question about your document..."
                : "Upload and select a document first..."
            }
            disabled={
              !documentId ||
              askQuestionMutation.isPending
            }
            rows={4}
            className="w-full resize-none rounded-xl border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-200 outline-none transition placeholder:text-slate-600 focus:border-indigo-500/60 focus:ring-2 focus:ring-indigo-500/10 disabled:cursor-not-allowed disabled:opacity-50"
          />

          <div className="mt-4 flex items-center justify-between gap-4">
            <p className="text-xs text-slate-600">
              Document-grounded answers with source references.
            </p>

            <button
              type="submit"
              disabled={
                !documentId ||
                !question.trim() ||
                askQuestionMutation.isPending
              }
              className="rounded-xl bg-indigo-500 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {askQuestionMutation.isPending
                ? "Thinking..."
                : "Ask Question"}
            </button>
          </div>
        </form>

        {askQuestionMutation.isPending && (
          <div className="mt-6 rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-4 text-sm text-indigo-400">
            Searching your document and generating an answer...
          </div>
        )}

        {askQuestionMutation.isError && (
          <div className="mt-6 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
            {askQuestionMutation.error.message}
          </div>
        )}

        {result && !askQuestionMutation.isPending && (
          <div className="mt-8">
            <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-5">
              <p className="text-xs font-medium uppercase tracking-wider text-emerald-400">
                AI Answer
              </p>

              <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-300">
                {result.answer}
              </p>
            </div>

            {result.sources.length > 0 && (
              <div className="mt-5">
                <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
                  Sources
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {result.sources.map(
                    (source, index) => (
                      <div
                        key={`${source.filename}-${source.page_number}-${index}`}
                        className="rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-xs text-slate-400"
                      >
                        <span className="text-slate-200">
                          {source.filename}
                        </span>

                        <span className="mx-1 text-slate-600">
                          ·
                        </span>

                        Page {source.page_number}
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default QuestionPanel;