"""Estimate a model bill on your computer, before any API call.

This is the calculator from week_2/lesson09_token_cost_guide.ipynb.
Counting tokens and multiplying by a price does not contact OpenRouter,
Gemini, or any other provider.

Prices below are the sample list in that notebook (plus the Gemini price
the Week 3 office-hours notebook already used). They go out of date.
Check https://openrouter.ai/models before a large run.
"""

from __future__ import annotations

# Dollars per 1 million tokens: (input, output).
CHAT_PRICES = {
    "z-ai/glm-5.3-flash": (0.036, 0.5),
    "qwen/qwen3-8b": (0.12, 0.46),
    "deepseek/deepseek-chat-v3.1": (0.14, 0.28),
    "anthropic/claude-haiku-4.5": (1.00, 5.00),
    "anthropic/claude-sonnet-4.5": (3.00, 15.00),
    # Week 3 office hours calls Gemini directly, not through OpenRouter.
    "gemini-3.5-flash-lite": (0.30, 2.50),
}

# Embedding models are not in the Week 2 price table.
# Fill a number from https://openrouter.ai/models if you want dollars.
EMBEDDING_PRICE_PER_1M = {}

_encoder = None
_token_method = "about 4 characters per token"


def estimate_tokens_quick(text: str) -> int:
    """Rough token estimate: about 4 characters per token for English text."""
    return max(1, len(text) // 4)


def count_tokens(text: str) -> int:
    """Count tokens locally. Uses tiktoken when it is installed, otherwise 4 characters per token."""
    global _encoder, _token_method
    if _encoder is None and _token_method != "rough character count":
        try:
            import tiktoken

            _encoder = tiktoken.get_encoding("o200k_base")
            _token_method = "tiktoken o200k_base, a close guess for the course model"
        except Exception:
            _encoder = False
            _token_method = "rough character count"
    if _encoder:
        return len(_encoder.encode(text))
    return estimate_tokens_quick(text)


def estimate_cost(
    num_items,
    input_tokens_per_item,
    output_tokens,
    price_per_1m_input,
    price_per_1m_output,
) -> float:
    """Same dollar formula as Week 2's token cost guide."""
    input_cost = (num_items * input_tokens_per_item / 1_000_000) * price_per_1m_input
    output_cost = (num_items * output_tokens / 1_000_000) * price_per_1m_output
    return input_cost + output_cost


def _money(amount: float) -> str:
    return f"${amount:.6f}"


def _as_prompts(prompts) -> list[str]:
    if isinstance(prompts, str):
        return [prompts]
    return [str(p) for p in prompts]


def preview_llm_cost(
    prompts,
    model: str,
    assumed_output_tokens: int = 100,
    max_output_tokens: int | None = None,
    label: str = "this batch",
    price_per_1m_input: float | None = None,
    price_per_1m_output: float | None = None,
) -> float | None:
    """Print an estimated dollar cost. Does not call a model API.

    `assumed_output_tokens` is a guess. The real reply length is unknown
    until the model writes it. Raise the guess if you expect a long answer.
    """
    texts = _as_prompts(prompts)
    print(f"{label}")
    if not texts:
        print("No prompts, so the estimated cost is $0.000000.")
        print("This cell did not call the model API.")
        return 0.0

    input_counts = [count_tokens(text) for text in texts]
    total_input = sum(input_counts)
    print(f"{len(texts)} call(s) to {model}")
    print(f"Input tokens counted on this computer ({_token_method}): {total_input}")

    if price_per_1m_input is None or price_per_1m_output is None:
        pair = CHAT_PRICES.get(model)
        if pair is None:
            print(f"No sample price is saved for {model}.")
            print("Look up input and output dollars per 1 million tokens at https://openrouter.ai/models")
            print("Then pass price_per_1m_input= and price_per_1m_output= to this function.")
            print("This cell did not call the model API.")
            return None
        price_per_1m_input, price_per_1m_output = pair

    typical = (total_input / 1_000_000) * price_per_1m_input
    typical += (len(texts) * assumed_output_tokens / 1_000_000) * price_per_1m_output
    print(
        f"Estimated cost if each reply is about {assumed_output_tokens} tokens: {_money(typical)}"
    )
    print(
        f"Sample price used: ${price_per_1m_input:.2f} per 1M input tokens, "
        f"${price_per_1m_output:.2f} per 1M output tokens."
    )
    if max_output_tokens is not None:
        ceiling = (total_input / 1_000_000) * price_per_1m_input
        ceiling += (len(texts) * max_output_tokens / 1_000_000) * price_per_1m_output
        print(
            f"Ceiling if every reply uses {max_output_tokens} tokens: {_money(ceiling)}"
        )
    print("Prices change. Check https://openrouter.ai/models before a large run.")
    print("This cell did not call the model API.")
    return typical


def preview_embedding_cost(
    texts,
    model: str,
    price_per_1m_input: float | None = None,
    label: str = "embeddings",
) -> float | None:
    """Print an estimated embedding cost. Does not call a model API.

    Embedding calls are priced on input tokens. There is no reply to guess.
    """
    items = _as_prompts(texts)
    total_input = sum(count_tokens(text) for text in items) if items else 0
    print(f"{label}")
    print(f"{len(items)} text(s) to {model}")
    print(f"Input tokens counted on this computer ({_token_method}): {total_input}")

    price = EMBEDDING_PRICE_PER_1M.get(model) if price_per_1m_input is None else price_per_1m_input
    if price is None:
        print(f"No sample price is saved for {model}.")
        print("Look up dollars per 1 million input tokens at https://openrouter.ai/models")
        print("Then call preview_embedding_cost(..., price_per_1m_input=THAT_NUMBER).")
        print("This cell did not call the model API.")
        return None

    cost = (total_input / 1_000_000) * price
    print(f"Estimated cost: {_money(cost)}")
    print("This cell did not call the model API.")
    return cost


def _self_check() -> None:
    # Week 2 notebook: 500 items, 46 input tokens, 398 output tokens, course default prices
    typical = estimate_cost(500, 46, 398, 0.036, 0.5)
    if abs(typical - 0.100328) > 0.000001:
        raise SystemExit(f"estimate_cost drifted from the Week 2 example: {typical}")
    if count_tokens("hello") < 1:
        raise SystemExit("count_tokens failed")


if __name__ == "__main__":
    _self_check()
    print("llm_cost self-check passed")
