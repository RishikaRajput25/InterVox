import { Link } from "react-router-dom";
import {
  ArrowLeft,
  FileText,
  Mic,
  ShieldCheck,
  Upload,
} from "lucide-react";

import DocumentUploader from "../components/documents/DocumentUploader";

function Documents() {
  return (
    <main className="intervox-shell min-h-screen text-white">
      <div className="intervox-background" />

      <div className="relative z-10 flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] bg-[#0c1424]/75 px-5 py-6 backdrop-blur-xl lg:flex lg:flex-col">
          <div className="flex items-center gap-3 px-2">
            <div className="intervox-logo">
              <span />
              <span />
              <span />
              <span />
            </div>

            <span className="text-lg font-semibold tracking-tight">
              InterVox
            </span>
          </div>

          <p className="mt-1 px-2 text-[11px] uppercase tracking-[0.2em] text-slate-500">
            AI Research Assistant
          </p>

          <nav className="mt-10 space-y-2">
            <div className="intervox-nav-item intervox-nav-active">
              <FileText
                size={17}
                strokeWidth={1.8}
              />

              <span>Documents</span>
            </div>

            <Link
              to="/"
              className="intervox-nav-item"
            >
              <Mic
                size={17}
                strokeWidth={1.8}
              />

              <span>Voice Assistant</span>
            </Link>
          </nav>

          <div className="mt-auto rounded-2xl border border-white/[0.06] bg-white/[0.025] p-4">
            <p className="text-xs leading-5 text-slate-500">
              Upload your research material and InterVox will prepare it
              for voice-based conversations.
            </p>
          </div>
        </aside>

        {/* Main */}
        <section className="flex min-w-0 flex-1 flex-col">
          {/* Header */}
          <header className="flex items-center justify-between px-6 py-5 sm:px-10">
            <Link
              to="/"
              className="intervox-back-button"
            >
              <ArrowLeft size={16} />
              Back to assistant
            </Link>

            <div className="intervox-status">
              <span className="intervox-status-dot" />
              Secure workspace
            </div>
          </header>

          {/* Content */}
          <div className="flex flex-1 items-center justify-center px-5 pb-12">
            <div className="w-full max-w-4xl">

              <div className="mb-10 text-center">
                <p className="intervox-eyebrow">
                  DOCUMENT WORKSPACE
                </p>

                <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
                  Your research starts here.
                </h1>

                <p className="mx-auto mt-4 max-w-xl text-sm leading-6 text-slate-400 sm:text-base">
                  Upload a document and InterVox will extract, process and
                  prepare its content for natural voice-based research.
                </p>
              </div>

              {/* Upload panel */}
              <div className="intervox-upload-panel">
                <div className="intervox-upload-icon">
                  <Upload size={23} />
                </div>

                <DocumentUploader />
              </div>

              {/* Supported formats */}
              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <div className="intervox-mini-badge">
                  <FileText size={14} />
                  PDF
                </div>

                <div className="intervox-mini-badge">
                  <FileText size={14} />
                  DOCX
                </div>

                <div className="intervox-mini-badge">
                  <FileText size={14} />
                  TXT
                </div>

                <div className="intervox-mini-badge">
                  <ShieldCheck size={14} />
                  Max 10 MB
                </div>
              </div>

            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

export default Documents;