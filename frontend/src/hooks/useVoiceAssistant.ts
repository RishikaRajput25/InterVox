// import {
//   useCallback,
//   useEffect,
//   useRef,
//   useState,
// } from "react";

// type VoiceState =
//   | "idle"
//   | "listening"
//   | "processing"
//   | "speaking";

// interface UseVoiceAssistantOptions {
//   documentId: string | null;
// }

// interface VoiceAssistantResult {
//   state: VoiceState;
//   transcript: string;
//   error: string | null;
//   startListening: () => Promise<void>;
//   stopListening: () => void;
// }

// const WS_BASE_URL =
//   import.meta.env.VITE_WS_BASE_URL;

// export function useVoiceAssistant({
//   documentId,
// }: UseVoiceAssistantOptions): VoiceAssistantResult {
//   const websocketRef =
//     useRef<WebSocket | null>(null);

//   const mediaRecorderRef =
//     useRef<MediaRecorder | null>(null);

//   const mediaStreamRef =
//     useRef<MediaStream | null>(null);

//   const audioRef =
//     useRef<HTMLAudioElement | null>(null);

//   const audioChunksRef =
//     useRef<Blob[]>([]);

//   const [state, setState] =
//     useState<VoiceState>("idle");

//   const [transcript, setTranscript] =
//     useState("");

//   const [error, setError] =
//     useState<string | null>(null);

//   const stopAudioPlayback =
//     useCallback(() => {
//       const audio =
//         audioRef.current;

//       if (!audio) {
//         return;
//       }

//       audio.pause();
//       audio.currentTime = 0;

//       if (audio.src) {
//         URL.revokeObjectURL(audio.src);
//         audio.src = "";
//       }
//     }, []);

//   const cleanupRecorder =
//     useCallback(() => {
//       const recorder =
//         mediaRecorderRef.current;

//       if (
//         recorder &&
//         recorder.state !== "inactive"
//       ) {
//         recorder.stop();
//       }

//       mediaRecorderRef.current = null;

//       const stream =
//         mediaStreamRef.current;

//       if (stream) {
//         stream
//           .getTracks()
//           .forEach((track) =>
//             track.stop()
//           );
//       }

//       mediaStreamRef.current = null;
//     }, []);

//   const stopListening =
//     useCallback(() => {
//       const websocket =
//         websocketRef.current;

//       cleanupRecorder();

//       if (
//         websocket &&
//         websocket.readyState === WebSocket.OPEN
//       ) {
//         websocket.send(
//           JSON.stringify({
//             type: "audio_end",
//           })
//         );
//       }

//       setState("idle");
//     }, [cleanupRecorder]);

//   const startListening =
//     useCallback(async () => {
//       if (!documentId) {
//         setError(
//           "Please select a document first."
//         );
//         return;
//       }

//       setError(null);

//       stopAudioPlayback();

//       try {
//         const stream =
//           await navigator.mediaDevices.getUserMedia(
//             {
//               audio: true,
//             }
//           );

//         mediaStreamRef.current =
//           stream;

//         const websocket =
//           new WebSocket(
//             `${WS_BASE_URL}/ws/voice`
//           );

//         websocket.binaryType =
//           "arraybuffer";

//         websocketRef.current =
//           websocket;

//         websocket.onopen = () => {
//           websocket.send(
//             JSON.stringify({
//               type: "audio_start",
//             })
//           );

//           const mimeType =
//             MediaRecorder.isTypeSupported(
//               "audio/webm;codecs=opus"
//             )
//               ? "audio/webm;codecs=opus"
//               : "audio/webm";

//           const recorder =
//             new MediaRecorder(
//               stream,
//               {
//                 mimeType,
//               }
//             );

//           mediaRecorderRef.current =
//             recorder;

//           recorder.ondataavailable =
//             async (event) => {
//               if (
//                 event.data.size === 0 ||
//                 websocket.readyState !==
//                   WebSocket.OPEN
//               ) {
//                 return;
//               }

//               const buffer =
//                 await event.data.arrayBuffer();

//               websocket.send(buffer);
//             };

//           recorder.onstop = () => {
//             if (
//               websocket.readyState ===
//               WebSocket.OPEN
//             ) {
//               websocket.send(
//                 JSON.stringify({
//                   type: "audio_end",
//                 })
//               );
//             }
//           };

//           recorder.start(250);

//           setState("listening");
//         };

//         websocket.onmessage =
//           async (event) => {
//             if (
//               typeof event.data ===
//               "string"
//             ) {
//               const message =
//                 JSON.parse(
//                   event.data
//                 );

//               if (
//                 message.type ===
//                 "transcript"
//               ) {
//                 setTranscript(
//                   message.text
//                 );

//                 setState(
//                   "processing"
//                 );
//               }

//               if (
//                 message.type ===
//                 "turn_started"
//               ) {
//                 setState(
//                   "processing"
//                 );
//               }

//               if (
//                 message.type ===
//                 "turn_cancelled"
//               ) {
//                 stopAudioPlayback();

//                 audioChunksRef.current =
//                   [];

//                 setState("idle");
//               }

//               if (
//                 message.type ===
//                 "error"
//               ) {
//                 setError(
//                   message.message
//                 );

//                 setState("idle");
//               }

//               if (
//                 message.type ===
//                 "response_complete"
//               ) {
//                 if (
//                   audioChunksRef
//                     .current.length > 0
//                 ) {
//                   const blob =
//                     new Blob(
//                       audioChunksRef.current,
//                       {
//                         type: "audio/mpeg",
//                       }
//                     );

//                   const url =
//                     URL.createObjectURL(
//                       blob
//                     );

//                   const audio =
//                     new Audio(url);

//                   audioRef.current =
//                     audio;

//                   audio.onended = () => {
//                     URL.revokeObjectURL(
//                       url
//                     );

//                     audioRef.current =
//                       null;

//                     audioChunksRef.current =
//                       [];

//                     setState("idle");
//                   };

//                   setState(
//                     "speaking"
//                   );

//                   await audio.play();
//                 } else {
//                   setState("idle");
//                 }
//               }
//             } else {
//               audioChunksRef.current.push(
//                 new Blob([
//                   event.data,
//                 ])
//               );

//               setState(
//                 "speaking"
//               );
//             }
//           };

//         websocket.onerror = () => {
//           setError(
//             "Voice connection failed."
//           );

//           setState("idle");
//         };

//         websocket.onclose = () => {
//           cleanupRecorder();
//         };
//       } catch (voiceError) {
//         cleanupRecorder();

//         setError(
//           voiceError instanceof Error
//             ? voiceError.message
//             : "Microphone access failed."
//         );

//         setState("idle");
//       }
//     }, [
//       cleanupRecorder,
//       documentId,
//       stopAudioPlayback,
//     ]);

//   useEffect(() => {
//     return () => {
//       stopAudioPlayback();
//       cleanupRecorder();

//       websocketRef.current?.close();
//       websocketRef.current = null;
//     };
//   }, [
//     cleanupRecorder,
//     stopAudioPlayback,
//   ]);

//   return {
//     state,
//     transcript,
//     error,
//     startListening,
//     stopListening,
//   };
// }


import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

type VoiceState =
  | "idle"
  | "listening"
  | "processing"
  | "speaking";

interface UseVoiceAssistantOptions {
  documentId: string | null;
}

interface UseVoiceAssistantResult {
  state: VoiceState;
  transcript: string;
  error: string | null;
  startListening: () => Promise<void>;
  stopListening: () => void;
}

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL;

export function useVoiceAssistant({
  documentId,
}: UseVoiceAssistantOptions): UseVoiceAssistantResult {
  const websocketRef =
    useRef<WebSocket | null>(null);

  const mediaRecorderRef =
    useRef<MediaRecorder | null>(null);

  const mediaStreamRef =
    useRef<MediaStream | null>(null);

  const audioRef =
    useRef<HTMLAudioElement | null>(null);

  const audioChunksRef =
    useRef<Blob[]>([]);

  // Prevent duplicate audio_end messages
  const audioEndSentRef =
    useRef(false);

  // Used to identify the current voice session
  const sessionIdRef =
    useRef(0);

  // Keep latest state available inside callbacks
  const stateRef =
    useRef<VoiceState>("idle");

  const [state, setState] =
    useState<VoiceState>("idle");

  const [transcript, setTranscript] =
    useState("");

  const [error, setError] =
    useState<string | null>(null);

  const updateState = useCallback(
    (nextState: VoiceState) => {
      stateRef.current = nextState;
      setState(nextState);
    },
    []
  );

  /*
   * Stop currently playing AI audio
   */
  const stopAudioPlayback =
    useCallback(() => {
      const audio =
        audioRef.current;

      if (!audio) {
        return;
      }

      console.log(
        "⏹️ Stopping AI audio playback"
      );

      audio.pause();
      audio.currentTime = 0;

      if (audio.src) {
        URL.revokeObjectURL(
          audio.src
        );

        audio.src = "";
      }

      audioRef.current = null;
    }, []);

  /*
   * Stop microphone tracks
   */
  const stopMediaStream =
    useCallback(() => {
      const stream =
        mediaStreamRef.current;

      if (!stream) {
        return;
      }

      console.log(
        "🎙️ Stopping microphone tracks"
      );

      stream
        .getTracks()
        .forEach((track) => {
          track.stop();
        });

      mediaStreamRef.current =
        null;
    }, []);

  /*
   * Close existing websocket
   */
  const closeWebSocket =
    useCallback(() => {
      const websocket =
        websocketRef.current;

      if (!websocket) {
        return;
      }

      if (
        websocket.readyState ===
        WebSocket.OPEN
      ) {
        console.log(
          "🔌 Closing existing WebSocket"
        );

        websocket.close();
      } else if (
        websocket.readyState ===
        WebSocket.CONNECTING
      ) {
        websocket.close();
      }

      websocketRef.current =
        null;
    }, []);

  /*
   * Cleanup recorder WITHOUT sending audio_end.
   *
   * Important:
   * recorder.stop() triggers onstop.
   * onstop itself sends audio_end.
   *
   * Therefore we never manually send audio_end
   * from cleanup.
   */
  const cleanupRecorder =
    useCallback(() => {
      const recorder =
        mediaRecorderRef.current;

      if (recorder) {
        console.log(
          "🧹 Cleaning MediaRecorder:",
          recorder.state
        );

        if (
          recorder.state !==
          "inactive"
        ) {
          recorder.stop();
        }

        mediaRecorderRef.current =
          null;
      }

      stopMediaStream();
    }, [
      stopMediaStream,
    ]);

  /*
   * Stop current listening session
   */
  const stopListening =
    useCallback(() => {
      console.log(
        "🛑 stopListening called"
      );

      const websocket =
        websocketRef.current;

      const recorder =
        mediaRecorderRef.current;

      /*
       * If recorder is active,
       * recorder.onstop will send audio_end.
       */
      if (
        recorder &&
        recorder.state !==
          "inactive"
      ) {
        console.log(
          "⏹️ Stopping recorder..."
        );

        updateState(
          "processing"
        );

        recorder.stop();

        stopMediaStream();

        return;
      }

      /*
       * Fallback:
       * if recorder is already inactive but
       * audio_end has not been sent.
       */
      if (
        websocket &&
        websocket.readyState ===
          WebSocket.OPEN &&
        !audioEndSentRef.current
      ) {
        console.log(
          "📤 Sending audio_end manually"
        );

        websocket.send(
          JSON.stringify({
            type: "audio_end",
          })
        );

        audioEndSentRef.current =
          true;

        updateState(
          "processing"
        );
      }

      stopMediaStream();
    }, [
      stopMediaStream,
      updateState,
    ]);

  /*
   * Start a new voice session
   */
  const startListening =
    useCallback(async () => {
      console.log(
        "🎤 startListening called"
      );

      console.log(
        "📄 documentId:",
        documentId
      );

      if (!documentId) {
        setError(
          "Please select a document first."
        );

        console.log(
          "❌ No document selected"
        );

        return;
      }

      /*
       * Prevent accidental double start.
       */
      if (
        stateRef.current ===
        "listening"
      ) {
        console.log(
          "⚠️ Already listening"
        );

        return;
      }

      /*
       * Create a new session ID.
       */
      const sessionId =
        sessionIdRef.current + 1;

      sessionIdRef.current =
        sessionId;

      console.log(
        "🆕 Voice session:",
        sessionId
      );

      /*
       * Clean any previous resources.
       */
      stopAudioPlayback();

      cleanupRecorder();

      closeWebSocket();

      audioChunksRef.current =
        [];

      audioEndSentRef.current =
        false;

      setError(null);

      try {
        /*
         * Request microphone
         */
        console.log(
          "🎙️ Requesting microphone..."
        );

        const stream =
          await navigator.mediaDevices.getUserMedia(
            {
              audio: true,
            }
          );

        /*
         * User may have started another session
         * while microphone permission was resolving.
         */
        if (
          sessionId !==
          sessionIdRef.current
        ) {
          console.log(
            "⚠️ Old microphone request ignored"
          );

          stream
            .getTracks()
            .forEach((track) =>
              track.stop()
            );

          return;
        }

        console.log(
          "✅ Microphone access granted"
        );

        mediaStreamRef.current =
          stream;

        /*
         * Create websocket
         */
        const websocket =
          new WebSocket(
            `${WS_BASE_URL}/ws/voice`
          );

        console.log(
          "🔌 WebSocket connecting:",
          `${WS_BASE_URL}/ws/voice`
        );

        websocket.binaryType =
          "arraybuffer";

        websocketRef.current =
          websocket;

        /*
         * WebSocket OPEN
         */
        websocket.onopen = () => {
          /*
           * Ignore stale socket
           */
          if (
            sessionId !==
            sessionIdRef.current
          ) {
            console.log(
              "⚠️ Ignoring stale WebSocket"
            );

            websocket.close();

            return;
          }

          console.log(
            "✅ WebSocket OPEN"
          );

          /*
           * Reset audio state
           */
          audioEndSentRef.current =
            false;

          audioChunksRef.current =
            [];

          /*
           * Tell backend that audio
           * recording is starting.
           */
          websocket.send(
            JSON.stringify({
              type: "audio_start",
            })
          );

          console.log(
            "📤 Sent audio_start"
          );

          /*
           * Select browser-supported MIME type.
           */
          const mimeType =
            MediaRecorder.isTypeSupported(
              "audio/webm;codecs=opus"
            )
              ? "audio/webm;codecs=opus"
              : "audio/webm";

          console.log(
            "🎵 MediaRecorder MIME:",
            mimeType
          );

          const recorder =
            new MediaRecorder(
              stream,
              {
                mimeType,
              }
            );

          mediaRecorderRef.current =
            recorder;

          /*
           * Recorder started
           */
          recorder.onstart = () => {
            console.log(
              "▶️ MediaRecorder STARTED"
            );

            updateState(
              "listening"
            );
          };

          /*
           * Audio chunks
           */
          recorder.ondataavailable =
            async (event) => {
              /*
               * Ignore stale session
               */
              if (
                sessionId !==
                sessionIdRef.current
              ) {
                return;
              }

              console.log(
                "🎧 Audio chunk:",
                event.data.size,
                "bytes"
              );

              if (
                event.data.size === 0
              ) {
                console.log(
                  "⚠️ Empty audio chunk skipped"
                );

                return;
              }

              if (
                websocket.readyState !==
                WebSocket.OPEN
              ) {
                console.log(
                  "⚠️ WebSocket not open, chunk skipped"
                );

                return;
              }

              try {
                const buffer =
                  await event.data.arrayBuffer();

                /*
                 * Check again after async conversion.
                 */
                if (
                  sessionId !==
                  sessionIdRef.current
                ) {
                  return;
                }

                if (
                  websocket.readyState !==
                  WebSocket.OPEN
                ) {
                  return;
                }

                websocket.send(
                  buffer
                );

                console.log(
                  "📤 Audio chunk sent:",
                  buffer.byteLength,
                  "bytes"
                );
              } catch (error) {
                console.error(
                  "❌ Failed to send audio chunk:",
                  error
                );
              }
            };

          /*
           * Recorder error
           */
          recorder.onerror = (
            event
          ) => {
            console.error(
              "❌ MediaRecorder ERROR:",
              event
            );

            setError(
              "Microphone recording failed."
            );

            updateState(
              "idle"
            );
          };

          /*
           * Recorder stopped
           *
           * THIS is the only normal place
           * where audio_end is sent.
           */
          recorder.onstop = () => {
            console.log(
              "⏹️ MediaRecorder STOPPED"
            );

            mediaRecorderRef.current =
              null;

            stopMediaStream();

            /*
             * Prevent duplicate audio_end.
             */
            if (
              audioEndSentRef.current
            ) {
              console.log(
                "⚠️ audio_end already sent"
              );

              return;
            }

            if (
              websocket.readyState ===
              WebSocket.OPEN
            ) {
              websocket.send(
                JSON.stringify({
                  type: "audio_end",
                })
              );

              audioEndSentRef.current =
                true;

              console.log(
                "📤 Sent audio_end"
              );
            } else {
              console.log(
                "⚠️ Cannot send audio_end, WebSocket closed"
              );
            }
          };

          /*
           * Start recording.
           *
           * 250ms gives frequent audio chunks.
           */
          recorder.start(250);

          console.log(
            "🎤 Recording started"
          );
        };

        /*
         * WebSocket messages
         */
        websocket.onmessage =
          async (event) => {
            /*
             * Ignore messages from old socket.
             */
            if (
              sessionId !==
              sessionIdRef.current
            ) {
              console.log(
                "⚠️ Ignoring stale WebSocket message"
              );

              return;
            }

            /*
             * Text / JSON message
             */
            if (
              typeof event.data ===
              "string"
            ) {
              console.log(
                "📩 WebSocket message received:",
                event.data
              );

              let message: any;

              try {
                message =
                  JSON.parse(
                    event.data
                  );
              } catch (error) {
                console.error(
                  "❌ Invalid server message:",
                  error
                );

                return;
              }

              console.log(
                "📨 Server message:",
                message
              );

              /*
               * Initial backend cancellation
               *
               * The backend currently sends
               * turn_cancelled when audio_start
               * is received because it cancels
               * any previous turn.
               *
               * IMPORTANT:
               * Do NOT set idle while we are
               * actively listening.
               */
              if (
                message.type ===
                "turn_cancelled"
              ) {
                console.log(
                  "🛑 TURN CANCELLED:",
                  message.turn_id
                );

                if (
                  stateRef.current ===
                  "listening"
                ) {
                  console.log(
                    "ℹ️ Ignoring initial cancellation while listening"
                  );

                  return;
                }

                /*
                 * Cancellation during another
                 * state means current response
                 * should stop.
                 */
                stopAudioPlayback();

                audioChunksRef.current =
                  [];

                updateState(
                  "idle"
                );

                return;
              }

              /*
               * Transcript
               */
              if (
                message.type ===
                "transcript"
              ) {
                console.log(
                  "📝 TRANSCRIPT:",
                  message.text
                );

                setTranscript(
                  message.text
                );

                updateState(
                  "processing"
                );

                return;
              }

              /*
               * Turn started
               */
              if (
                message.type ===
                "turn_started"
              ) {
                console.log(
                  "🚀 TURN STARTED"
                );

                updateState(
                  "processing"
                );

                return;
              }

              /*
               * Server error
               */
              if (
                message.type ===
                "error"
              ) {
                console.error(
                  "❌ Server error:",
                  message.message
                );

                setError(
                  message.message ||
                    "Voice processing failed."
                );

                stopAudioPlayback();

                audioChunksRef.current =
                  [];

                updateState(
                  "idle"
                );

                return;
              }

              /*
               * AI response complete
               */
              if (
                message.type ===
                "response_complete"
              ) {
                console.log(
                  "🔊 RESPONSE COMPLETE"
                );

                if (
                  audioChunksRef.current
                    .length === 0
                ) {
                  console.log(
                    "⚠️ Response complete but no audio chunks"
                  );

                  updateState(
                    "idle"
                  );

                  return;
                }

                console.log(
                  "🎵 Audio chunks:",
                  audioChunksRef.current
                    .length
                );

                const blob =
                  new Blob(
                    audioChunksRef.current,
                    {
                      type: "audio/mpeg",
                    }
                  );

                const url =
                  URL.createObjectURL(
                    blob
                  );

                const audio =
                  new Audio(url);

                audioRef.current =
                  audio;

                /*
                 * Audio finished
                 */
                audio.onended = () => {
                  console.log(
                    "🔚 Audio playback ended"
                  );

                  URL.revokeObjectURL(
                    url
                  );

                  if (
                    audioRef.current ===
                    audio
                  ) {
                    audioRef.current =
                      null;
                  }

                  audioChunksRef.current =
                    [];

                  updateState(
                    "idle"
                  );
                };

                /*
                 * Audio error
                 */
                audio.onerror = () => {
                  console.error(
                    "❌ Audio playback error"
                  );

                  URL.revokeObjectURL(
                    url
                  );

                  if (
                    audioRef.current ===
                    audio
                  ) {
                    audioRef.current =
                      null;
                  }

                  audioChunksRef.current =
                    [];

                  setError(
                    "Could not play AI voice."
                  );

                  updateState(
                    "idle"
                  );
                };

                updateState(
                  "speaking"
                );

                console.log(
                  "▶️ Playing AI voice..."
                );

                try {
                  await audio.play();
                } catch (error) {
                  console.error(
                    "❌ Audio playback failed:",
                    error
                  );

                  URL.revokeObjectURL(
                    url
                  );

                  if (
                    audioRef.current ===
                    audio
                  ) {
                    audioRef.current =
                      null;
                  }

                  audioChunksRef.current =
                    [];

                  setError(
                    "Could not play AI voice."
                  );

                  updateState(
                    "idle"
                  );
                }

                return;
              }
            }

            /*
             * Binary audio
             */
            else {
              console.log(
                "🔊 BINARY AUDIO RECEIVED:",
                event.data.byteLength
              );

              audioChunksRef.current.push(
                new Blob([
                  event.data,
                ])
              );

              /*
               * Don't immediately play here.
               * Wait for response_complete.
               */
              updateState(
                "speaking"
              );
            }
          };

        /*
         * WebSocket error
         */
        websocket.onerror = (
          event
        ) => {
          /*
           * Ignore stale socket errors.
           */
          if (
            sessionId !==
            sessionIdRef.current
          ) {
            return;
          }

          console.error(
            "❌ WebSocket ERROR:",
            event
          );

          setError(
            "Voice connection failed."
          );

          stopMediaStream();

          updateState(
            "idle"
          );
        };

        /*
         * WebSocket closed
         */
        websocket.onclose = (
          event
        ) => {
          console.log(
            "🔌 WebSocket CLOSED:",
            event.code,
            event.reason
          );

          /*
           * Only clean current websocket.
           */
          if (
            websocketRef.current ===
            websocket
          ) {
            websocketRef.current =
              null;
          }

          /*
           * Don't unnecessarily change state
           * if the AI is already speaking.
           */
          if (
            stateRef.current ===
              "listening" ||
            stateRef.current ===
              "processing"
          ) {
            stopMediaStream();
          }
        };
      } catch (voiceError) {
        console.error(
          "❌ Voice error:",
          voiceError
        );

        cleanupRecorder();

        closeWebSocket();

        setError(
          voiceError instanceof Error
            ? voiceError.message
            : "Microphone access failed."
        );

        updateState(
          "idle"
        );
      }
    }, [
      cleanupRecorder,
      closeWebSocket,
      documentId,
      stopAudioPlayback,
      stopMediaStream,
      updateState,
    ]);

  /*
   * Cleanup when component unmounts
   */
  useEffect(() => {
    return () => {
      console.log(
        "🧹 Voice assistant unmount cleanup"
      );

      /*
       * Invalidate current session.
       */
      sessionIdRef.current += 1;

      stopAudioPlayback();

      cleanupRecorder();

      closeWebSocket();

      audioChunksRef.current =
        [];

      audioEndSentRef.current =
        false;
    };
  }, [
    cleanupRecorder,
    closeWebSocket,
    stopAudioPlayback,
  ]);

  return {
    state,
    transcript,
    error,
    startListening,
    stopListening,
  };
}
