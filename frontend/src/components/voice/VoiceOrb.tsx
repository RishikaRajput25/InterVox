// interface VoiceOrbProps {
//   state?: "idle" | "listening" | "speaking";
// }

// function VoiceOrb({ state = "idle" }: VoiceOrbProps) {
//   const isListening = state === "listening";
//   const isSpeaking = state === "speaking";

//   return (
//     <div className="relative flex h-72 w-72 items-center justify-center">
//       {/* Outer pulse */}
//       <div
//         className={`absolute inset-0 rounded-full border transition-all duration-700 ${
//           isListening
//             ? "scale-110 border-indigo-400/40"
//             : isSpeaking
//               ? "scale-105 border-blue-400/40"
//               : "scale-100 border-slate-700"
//         }`}
//       />

//       {/* Glow */}
//       <div
//         className={`absolute h-52 w-52 rounded-full blur-3xl transition-all duration-700 ${
//           isListening
//             ? "bg-indigo-500/20"
//             : isSpeaking
//               ? "bg-blue-500/20"
//               : "bg-slate-500/10"
//         }`}
//       />

//       {/* Orb */}
//       <div
//         className={`relative flex h-44 w-44 items-center justify-center rounded-full border shadow-2xl transition-all duration-500 ${
//           isListening
//             ? "scale-105 border-indigo-400/50 bg-indigo-500/10"
//             : isSpeaking
//               ? "scale-105 border-blue-400/50 bg-blue-500/10"
//               : "border-slate-700 bg-slate-900"
//         }`}
//       >
//         <div className="h-24 w-24 rounded-full bg-slate-800/80 shadow-inner" />

//         {/* Center indicator */}
//         <div
//           className={`absolute h-3 w-3 rounded-full transition-all duration-300 ${
//             isListening
//               ? "bg-indigo-400 shadow-[0_0_20px_rgba(129,140,248,0.8)]"
//               : isSpeaking
//                 ? "bg-blue-400 shadow-[0_0_20px_rgba(96,165,250,0.8)]"
//                 : "bg-slate-500"
//           }`}
//         />
//       </div>
//     </div>
//   );
// }

// export default VoiceOrb;

interface VoiceOrbProps {
  state?: "idle" | "processing" | "ready" | "listening" | "speaking";
}

function VoiceOrb({ state = "idle" }: VoiceOrbProps) {
  const isListening = state === "listening";
  const isSpeaking = state === "speaking";
  const isProcessing = state === "processing";
  const isReady = state === "ready";

  return (
    <div
      className={`voice-orb voice-orb-${state}`}
      aria-label={`Voice assistant ${state}`}
    >
      {/* Ambient glow */}
      <div className="voice-orb-glow" />

      {/* Outer rings */}
      <div className="voice-orb-ring voice-orb-ring-1" />
      <div className="voice-orb-ring voice-orb-ring-2" />
      <div className="voice-orb-ring voice-orb-ring-3" />

      {/* Main orb */}
      <div className="voice-orb-core">

        {isProcessing ? (
          <div className="voice-orb-processing-icon">
            <span />
            <span />
            <span />
          </div>
        ) : isListening || isSpeaking ? (
          <div className="voice-wave">
            {Array.from({ length: 11 }).map((_, index) => (
              <span key={index} />
            ))}
          </div>
        ) : isReady ? (
          <div className="voice-ready-icon">
            <span>✓</span>
          </div>
        ) : (
          <div className="voice-wave voice-wave-idle">
            {Array.from({ length: 7 }).map((_, index) => (
              <span key={index} />
            ))}
          </div>
        )}

      </div>
    </div>
  );
}

export default VoiceOrb;