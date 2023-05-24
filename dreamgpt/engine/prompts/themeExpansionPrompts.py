import random

def themeExpansionPrompt(theme, count = 20):
    PROMPT_USER_INPUT = "Write a list of 3 things related to \"bicycling\". Be concise. I just need the names as a JSON list of strings."
    PROMPT_EXAMPLE = """["bicycle", "helmet", "pedals"]"""
    PROMPT_QUERY = f"Now generate {count} related to \"{theme}\"."

    return [
        {"role": "user", "content": PROMPT_USER_INPUT},
        {"role": "assistant", "content": PROMPT_EXAMPLE},
        {"role": "user", "content": PROMPT_QUERY}
      ]