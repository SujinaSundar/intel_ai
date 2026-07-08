from groq import Groq

from app.database.config import (
    settings
)


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(
    prompt: str
) -> str:
    """
    Generate answer using Groq.
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    return (
        response
        .choices[0]
        .message.content
    )
# Alias for compatibility
ask_llm = generate_answer