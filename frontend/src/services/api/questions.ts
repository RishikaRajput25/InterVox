import apiClient from "./client";

export interface QuestionRequest {
  question: string;
  document_id: string;
}

export interface QuestionSource {
  filename: string;
  page_number: number;
}

export interface QuestionResponse {
  answer: string;
  sources: QuestionSource[];
}

export async function askQuestion(
  request: QuestionRequest
): Promise<QuestionResponse> {
  const response = await apiClient.post<QuestionResponse>(
    "/questions/ask",
    request
  );

  return response.data;
}