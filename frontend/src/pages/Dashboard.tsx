
// import { Link } from "react-router-dom";
// import {
//   FileText,
//   Mic,
//   ArrowUpRight,
//   Sparkles,
//   ShieldCheck,
//   Square,
// } from "lucide-react";

// import VoiceOrb from "../components/voice/VoiceOrb";
// import QuestionPanel from "../components/questions/QuestionPanel";
// import { useDocumentStore } from "../stores/documentStore";
// import { useVoiceAssistant } from "../hooks/useVoiceAssistant";

// function Dashboard() {
//   const selectedDocument = useDocumentStore(
//     (state) => state.selectedDocument
//   );

//   const {
//     state: voiceState,
//     transcript,
//     error,
//     startListening,
//     stopListening,
//   } = useVoiceAssistant({
//     documentId: selectedDocument?.documentId ?? null,
//   });

//   const handleVoiceClick = async () => {
//     if (voiceState === "listening") {
//       stopListening();
//       return;
//     }

//     if (
//       voiceState === "processing" ||
//       voiceState === "speaking"
//     ) {
//       return;
//     }

//     await startListening();
//   };

//   return (
//     <main className="intervox-shell min-h-screen text-white">
//       <div className="intervox-background" />

//       <div className="relative z-10 flex min-h-screen">
//         {/* Sidebar */}
//         <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] bg-[#0c1424]/75 px-5 py-6 backdrop-blur-xl lg:flex lg:flex-col">
//           <div className="flex items-center gap-3 px-2">
//             <div className="intervox-logo">
//               <span />
//               <span />
//               <span />
//               <span />
//             </div>

//             <span className="text-lg font-semibold tracking-tight">
//               InterVox
//             </span>
//           </div>

//           <p className="mt-1 px-2 text-[11px] uppercase tracking-[0.2em] text-slate-500">
//             AI Research Assistant
//           </p>

//           <nav className="mt-10 space-y-2">
//             <Link
//               to="/documents"
//               className="intervox-nav-item group"
//             >
//               <FileText
//                 size={17}
//                 strokeWidth={1.8}
//                 className="text-indigo-300"
//               />

//               <span>Documents</span>

//               <ArrowUpRight
//                 size={14}
//                 className="ml-auto opacity-0 transition group-hover:opacity-60"
//               />
//             </Link>

//             <div className="intervox-nav-item intervox-nav-active">
//               <Mic
//                 size={17}
//                 strokeWidth={1.8}
//               />

//               <span>Voice Assistant</span>
//             </div>
//           </nav>

//           <div className="mt-auto rounded-2xl border border-white/[0.06] bg-white/[0.025] p-4">
//             <div className="mb-3 flex items-center gap-2">
//               <Sparkles
//                 size={15}
//                 className="text-indigo-300"
//               />

//               <span className="text-xs font-medium text-slate-300">
//                 Voice-first research
//               </span>
//             </div>

//             <p className="text-xs leading-5 text-slate-500">
//               Your documents.
//               <br />
//               Your voice.
//               <br />
//               Smarter answers.
//             </p>
//           </div>
//         </aside>

//         {/* Main content */}
//         <section className="flex min-w-0 flex-1 flex-col">
//           {/* Top bar */}
//           <header className="flex items-center justify-between px-6 py-5 sm:px-10">
//             <div className="lg:hidden">
//               <div className="flex items-center gap-3">
//                 <div className="intervox-logo">
//                   <span />
//                   <span />
//                   <span />
//                   <span />
//                 </div>

//                 <span className="font-semibold">
//                   InterVox
//                 </span>
//               </div>
//             </div>

//             <div className="hidden lg:block" />

//             <div className="intervox-status">
//               <span className="intervox-status-dot" />
//               Voice Research
//             </div>
//           </header>

//           {/* Hero + Research */}
//           <div className="flex flex-1 flex-col items-center px-5 pb-12 pt-4">
//             <div className="max-w-2xl text-center">
//               <p className="intervox-eyebrow">
//                 {voiceState === "listening"
//                   ? "LISTENING"
//                   : voiceState === "processing"
//                   ? "THINKING"
//                   : voiceState === "speaking"
//                   ? "RESPONDING"
//                   : "READY TO RESEARCH"}
//               </p>

//               <h1 className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-4xl lg:text-5xl">
//                 Ask your documents
//                 <span className="intervox-heading-accent">
//                   {" "}anything.
//                 </span>
//               </h1>

//               <p className="mx-auto mt-5 max-w-xl text-sm leading-6 text-slate-400 sm:text-base">
//                 Upload your research material and have a natural
//                 conversation with your documents using real-time voice.
//               </p>
//             </div>

//             {/* Voice Orb */}
//             <button
//               type="button"
//               onClick={handleVoiceClick}
//               disabled={
//                 voiceState === "processing" ||
//                 voiceState === "speaking" ||
//                 !selectedDocument
//               }
//               className="mt-10 cursor-pointer border-0 bg-transparent p-0 disabled:cursor-default"
//               aria-label={
//                 voiceState === "listening"
//                   ? "Stop listening"
//                   : "Start voice assistant"
//               }
//             >
//               <VoiceOrb
//                 state={
//                   voiceState === "idle"
//                     ? "idle"
//                     : voiceState
//                 }
//               />
//             </button>

//             {/* Voice control hint */}
//             {selectedDocument && (
//               <div className="mt-5 flex items-center gap-2 text-xs text-slate-500">
//                 {voiceState === "listening" ? (
//                   <>
//                     <Square size={11} fill="currentColor" />
//                     Click the orb to stop
//                   </>
//                 ) : voiceState === "processing" ? (
//                   "Processing your question..."
//                 ) : voiceState === "speaking" ? (
//                   "InterVox is responding..."
//                 ) : (
//                   <>
//                     <Mic size={13} />
//                     Click the orb to speak
//                   </>
//                 )}
//               </div>
//             )}

//             {/* Transcript */}
//             {transcript && (
//               <div className="mt-6 w-full max-w-2xl rounded-2xl border border-white/[0.07] bg-white/[0.025] px-5 py-4 text-left backdrop-blur-xl">
//                 <p className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
//                   You said
//                 </p>

//                 <p className="mt-2 text-sm leading-6 text-slate-200">
//                   {transcript}
//                 </p>
//               </div>
//             )}

//             {/* Error */}
//             {error && (
//               <div className="mt-5 w-full max-w-2xl rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-300">
//                 {error}
//               </div>
//             )}

//             {/* Selected document */}
//             {selectedDocument ? (
//               <div className="mt-8 flex items-center gap-3 rounded-xl border border-emerald-500/20 bg-emerald-500/5 px-4 py-3">
//                 <ShieldCheck
//                   size={16}
//                   className="text-emerald-400"
//                 />

//                 <div className="text-left">
//                   <p className="text-[11px] uppercase tracking-wider text-emerald-400">
//                     Active document
//                   </p>

//                   <p className="mt-0.5 max-w-xs truncate text-sm text-slate-200">
//                     {selectedDocument.filename}
//                   </p>
//                 </div>
//               </div>
//             ) : (
//               <Link
//                 to="/documents"
//                 className="intervox-primary-button mt-8"
//               >
//                 <FileText size={18} />
//                 Upload a document
//                 <ArrowUpRight size={16} />
//               </Link>
//             )}

//             {!selectedDocument && (
//               <p className="mt-4 text-xs text-slate-500">
//                 PDF, DOCX and TXT · Up to 10 MB
//               </p>
//             )}

//             {/* Research question panel */}
//             {selectedDocument && (
//               <div className="mt-10 w-full max-w-3xl">
//                 <QuestionPanel
//                   documentId={
//                     selectedDocument.documentId
//                   }
//                   documentName={
//                     selectedDocument.filename
//                   }
//                 />
//               </div>
//             )}

//             {/* Trust indicators */}
//             <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
//               <div className="intervox-mini-badge">
//                 <ShieldCheck size={14} />
//                 Document-based answers
//               </div>

//               <div className="intervox-mini-badge">
//                 <Mic size={14} />
//                 Voice-first interaction
//               </div>
//             </div>
//           </div>

//           {/* Footer */}
//           <footer className="px-6 pb-5 text-center text-[11px] text-slate-600">
//             InterVox · Your documents stay at the center of the conversation.
//           </footer>
//         </section>
//       </div>
//     </main>
//   );
// }

// export default Dashboard;


import { Link } from "react-router-dom";
import {
  FileText,
  Mic,
  ArrowUpRight,
  Sparkles,
  ShieldCheck,
  Square,
} from "lucide-react";

import VoiceOrb from "../components/voice/VoiceOrb";
import QuestionPanel from "../components/questions/QuestionPanel";
import { useDocumentStore } from "../stores/documentStore";
import { useVoiceAssistant } from "../hooks/useVoiceAssistant";

function Dashboard() {
  const selectedDocument = useDocumentStore(
    (state) => state.selectedDocument
  );

  const {
    state: voiceState,
    transcript,
    error,
    startListening,
    stopListening,
  } = useVoiceAssistant({
    documentId: selectedDocument?.documentId ?? null,
  });

  const handleVoiceClick = async () => {
    // If currently listening, stop recording
    if (voiceState === "listening") {
      stopListening();
      return;
    }

    // Don't start another turn while processing/speaking
    if (
      voiceState === "processing" ||
      voiceState === "speaking"
    ) {
      return;
    }

    // Start a new voice turn
    await startListening();
  };

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

          {/* Hero + Research */}
          <div className="flex flex-1 flex-col items-center px-5 pb-12 pt-4">
            <div className="max-w-2xl text-center">
              <p className="intervox-eyebrow">
                {voiceState === "listening"
                  ? "LISTENING"
                  : voiceState === "processing"
                  ? "THINKING"
                  : voiceState === "speaking"
                  ? "RESPONDING"
                  : "READY TO RESEARCH"}
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

            {/* Voice Orb */}
            <button
              type="button"
              onClick={handleVoiceClick}
              disabled={
                voiceState === "processing" ||
                voiceState === "speaking" ||
                !selectedDocument
              }
              className={`mt-10 border-0 bg-transparent p-0 ${
                voiceState === "listening"
                  ? "cursor-pointer"
                  : "cursor-pointer disabled:cursor-default"
              }`}
              aria-label={
                voiceState === "listening"
                  ? "Stop listening"
                  : "Start voice assistant"
              }
            >
              <VoiceOrb
                state={
                  voiceState === "idle"
                    ? "idle"
                    : voiceState
                }
              />
            </button>

            {/* Explicit Stop Button */}
            {voiceState === "listening" && (
              <button
                type="button"
                onClick={stopListening}
                className="mt-4 flex items-center gap-2 rounded-full border border-red-400/20 bg-red-500/10 px-4 py-2 text-xs font-medium text-red-300 transition hover:bg-red-500/20 hover:text-red-200"
              >
                <Square
                  size={11}
                  fill="currentColor"
                />

                Stop Listening
              </button>
            )}

            {/* Voice control hint */}
            {selectedDocument && (
              <div className="mt-5 flex items-center gap-2 text-xs text-slate-500">
                {voiceState === "listening" ? (
                  <>
                    <Square
                      size={11}
                      fill="currentColor"
                    />

                    Click the orb or button to stop
                  </>
                ) : voiceState === "processing" ? (
                  "Processing your question..."
                ) : voiceState === "speaking" ? (
                  "InterVox is responding..."
                ) : (
                  <>
                    <Mic size={13} />
                    Click the orb to speak
                  </>
                )}
              </div>
            )}

            {/* Transcript */}
            {transcript && (
              <div className="mt-6 w-full max-w-2xl rounded-2xl border border-white/[0.07] bg-white/[0.025] px-5 py-4 text-left backdrop-blur-xl">
                <p className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
                  You said
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-200">
                  {transcript}
                </p>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="mt-5 w-full max-w-2xl rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* Selected document */}
            {selectedDocument ? (
              <div className="mt-8 flex items-center gap-3 rounded-xl border border-emerald-500/20 bg-emerald-500/5 px-4 py-3">
                <ShieldCheck
                  size={16}
                  className="text-emerald-400"
                />

                <div className="text-left">
                  <p className="text-[11px] uppercase tracking-wider text-emerald-400">
                    Active document
                  </p>

                  <p className="mt-0.5 max-w-xs truncate text-sm text-slate-200">
                    {selectedDocument.filename}
                  </p>
                </div>
              </div>
            ) : (
              <Link
                to="/documents"
                className="intervox-primary-button mt-8"
              >
                <FileText size={18} />

                Upload a document

                <ArrowUpRight size={16} />
              </Link>
            )}

            {!selectedDocument && (
              <p className="mt-4 text-xs text-slate-500">
                PDF, DOCX and TXT · Up to 10 MB
              </p>
            )}

            {/* Research question panel */}
            {selectedDocument && (
              <div className="mt-10 w-full max-w-3xl">
                <QuestionPanel
                  documentId={
                    selectedDocument.documentId
                  }
                  documentName={
                    selectedDocument.filename
                  }
                />
              </div>
            )}

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
