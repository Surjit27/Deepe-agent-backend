API_TOKEN_PROVIDER_TYPES = [
    {
        "id": "openai",
        "label": "OpenAI",
        "free_allowance": "Pay-as-you-go / trial credits",
        "best_for": "GPT-family models and tooling",
        "env_key": "OPENAI_API_KEY",
    },
    {
        "id": "gemini",
        "label": "Google AI Studio",
        "free_allowance": "Free rate-limited Gemini Flash",
        "best_for": "Multimodal apps and 1M-token context",
        "env_key": "GOOGLE_API_KEY",
    },
    {
        "id": "anthropic",
        "label": "Claude (Anthropic)",
        "free_allowance": "Tiered usage",
        "best_for": "Long-context reasoning and agents",
        "env_key": "ANTHROPIC_API_KEY",
    },
    {
        "id": "cursor",
        "label": "Cursor",
        "free_allowance": "Plan-based",
        "best_for": "IDE-integrated coding workflows",
        "env_key": "CURSOR_API_KEY",
    },
    {
        "id": "cerebras",
        "label": "Cerebras",
        "free_allowance": "Up to 1M tokens/day per model",
        "best_for": "High-volume daily testing and ultra-fast speed",
        "env_key": "CEREBRAS_API_KEY",
    },
    {
        "id": "groq",
        "label": "GroqCloud",
        "free_allowance": "Model-specific daily limits",
        "best_for": "Real-time voice and low-latency chatbots",
        "env_key": "GROQ_API_KEY",
    },
    {
        "id": "mistral",
        "label": "Mistral AI",
        "free_allowance": "Daily free quota / $10 monthly trial",
        "best_for": "European residency and coding models",
        "env_key": "MISTRAL_API_KEY",
    },
    {
        "id": "openrouter",
        "label": "OpenRouter",
        "free_allowance": "20 req/min, 50 req/day on :free models",
        "best_for": "Testing many open models with one key",
        "env_key": "OPENROUTER_API_KEY",
    },
]

PROVIDER_IDS = {row["id"] for row in API_TOKEN_PROVIDER_TYPES}