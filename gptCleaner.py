from openai import OpenAI

client = OpenAI(api_key="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")

def getCleanText(rawText):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Clean up the text, fix any grammatical errors, and fix the spacing."},
            {"role": "user", "content": rawText},
        ],
    )
    return completion.choices[0].message.content