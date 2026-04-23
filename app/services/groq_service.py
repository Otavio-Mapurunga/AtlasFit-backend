import time
from groq import APIStatusError
from app.config import groq_client


class GroqTemporaryUnavailableError(Exception):
    pass


class GroqServiceError(Exception):
    pass


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
BACKOFF_SECONDS = 2


def gerar_treino(prompt: str) -> str:
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8000,
                temperature=0.7,
            )
            text =response.choices[0].message.content
            if not text:
                raise GroqServiceError("O Qroq retornou uma resposta vazia.")
            return text

        except APIStatusError as exc:
            last_error = exc
            if exc.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
                continue

            if exc.status_code in {429, 503}:
                raise GroqTemporaryUnavailableError(
                    "Serviço Groq temporariamente indisponível. Tente novamente em instantes."
                ) from exc
            raise GroqServiceError(f"Falha no Groq (status {exc.status_code}).") from exc

        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
                continue
            raise GroqServiceError("Erro inesperado ao gerar treino com Groq.") from exc

    raise GroqServiceError("Não foi possível gerar treino após tentativas de retry.") from last_error
