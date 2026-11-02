
import time
from groq import Groq

from prompt import AFTER, BEFORE, EXAMPLES, TICKETS, check


# Select the LLM model
MODEL = "openai/gpt-oss-120b"

# Connect to Groq API
client = Groq()


def sort_ticket(system, text):

    messages = [
        {"role": "system", "content": system},
        *EXAMPLES,
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return (
        response.choices[0].message.content,
        response.usage
    )


def run(label, system):

    right = 0
    tokens_in = 0
    tokens_out = 0

    started = time.perf_counter()

    print("\n", label)

    for text, expected in TICKETS:

        answer, usage = sort_ticket(system, text)

        tokens_in += usage.prompt_tokens
        tokens_out += usage.completion_tokens

        result = check(answer)

        ok = result is not None and result.category == expected

        right += ok

        print(
            f"  {'OK' if ok else 'BAD'} "
            f"{expected:9} {answer}"
        )

    seconds = time.perf_counter() - started

    print(
        f"\nAccuracy: {right}/{len(TICKETS)}"
    )

    print("Input tokens:", tokens_in)
    print("Output tokens:", tokens_out)

    print(
        f"Average time per ticket: "
        f"{seconds / len(TICKETS):.2f} seconds"
    )


# Compare two system prompts
run("BEFORE PROMPT", BEFORE)

run("AFTER PROMPT", AFTER)
