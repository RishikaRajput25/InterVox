import { Link } from "react-router-dom";
import {
  FileText,
  Mic,
  ArrowUpRight,
  Sparkles,
  ShieldCheck,
} from "lucide-react";

import VoiceOrb from "../components/voice/VoiceOrb";

function Dashboard() {
  return (
    <main className="intervox-shell min-h-screen text-white">
      <div className="intervox-background" />

      <div className="relative z-10 flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] bg-[#0c1424]/75 px-5 py-6 backdrop-blur-xl lg:flex lg:flex-col">
          {/* Logo */}
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

          {/* Navigation */}
          <nav className="mt-10 space-y-2">
            <Link
              to="/documents"
              className="intervox-nav-item group"
            >
              <FileText
                size={17}
                strokeWidth={1.8}
                className="text-indigo-300"
              />

              <span>Documents</span>

              <ArrowUpRight
                size={14}
                className="ml-auto opacity-0 transition group-hover:opacity-60"
              />
            </Link>

            <div className="intervox-nav-item intervox-nav-active">
              <Mic
                size={17}
                strokeWidth={1.8}
              />

              <span>Voice Assistant</span>
            </div>
          </nav>

          {/* Bottom info */}
          <div className="mt-auto rounded-2xl border border-white/[0.06] bg-white/[0.025] p-4">
            <div className="mb-3 flex items-center gap-2">
              <Sparkles
                size={15}
                className="text-indigo-300"
              />

              <span className="text-xs font-medium text-slate-300">
                Voice-first research
              </span>
            </div>

            <p className="text-xs leading-5 text-slate-500">
              Your documents.
              <br />
              Your voice.
              <br />
              Smarter answers.
            </p>
          </div>
        </aside>

        {/* Main content */}
        <section className="flex min-w-0 flex-1 flex-col">
          {/* Top bar */}
          <header className="flex items-center justify-between px-6 py-5 sm:px-10">
            <div className="lg:hidden">
              <div className="flex items-center gap-3">
                <div className="intervox-logo">
                  <span />
                  <span />
                  <span />
                  <span />
                </div>

                <span className="font-semibold">
                  InterVox
                </span>
              </div>
            </div>

            <div className="hidden lg:block" />

            <div className="intervox-status">
              <span className="intervox-status-dot" />
              Voice Research
            </div>
          </header>

          {/* Hero */}
          <div className="flex flex-1 flex-col items-center justify-center px-5 pb-10">

            <div className="max-w-2xl text-center">
              <p className="intervox-eyebrow">
                READY TO RESEARCH
              </p>

              <h1 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-4xl lg:text-5xl">
                Ask your documents
                <span className="intervox-heading-accent">
                  {" "}anything.
                </span>
              </h1>

              <p className="mx-auto mt-5 max-w-xl text-sm leading-6 text-slate-400 sm:text-base">
                Upload your research material and have a natural
                conversation with your documents using real-time voice.
              </p>
            </div>

            {/* Orb */}
            <div className="mt-10 sm:mt-12">
              <VoiceOrb state="idle" />
            </div>

            {/* Main CTA */}
            <Link
              to="/documents"
              className="intervox-primary-button mt-8"
            >
              <FileText size={18} />
              Upload a document
              <ArrowUpRight size={16} />
            </Link>

            <p className="mt-4 text-xs text-slate-500">
              PDF, DOCX and TXT · Up to 10 MB
            </p>

            {/* Trust indicators */}
            <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
              <div className="intervox-mini-badge">
                <ShieldCheck size={14} />
                Document-based answers
              </div>

              <div className="intervox-mini-badge">
                <Mic size={14} />
                Voice-first interaction
              </div>
            </div>
          </div>

          {/* Footer */}
          <footer className="px-6 pb-5 text-center text-[11px] text-slate-600">
            InterVox · Your documents stay at the center of the conversation.
          </footer>
        </section>
      </div>
    </main>
  );
}

export default Dashboard;