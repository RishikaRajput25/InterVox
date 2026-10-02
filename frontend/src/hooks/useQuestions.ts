import { useMutation } from "@tanstack/react-query";

import {
  askQuestion,
  type QuestionRequest,
  type QuestionResponse,
} from "../services/api/questions";

export function useAskQuestion() {
  return useMutation<
    QuestionResponse,
    Error,
    QuestionRequest
  >({
    mutationFn: askQuestion,
  });
}