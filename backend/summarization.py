from openai import OpenAI


def summarize_text(text, constraints):
    client = OpenAI(api_key="API_KEY")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{constraints}:\n\n {text}"}
        ],
        max_tokens=1500,
        temperature=0.5
    )

    summary = response.choices[0].message.content
    return summary