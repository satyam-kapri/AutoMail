import openai


def generate_email(key,userprompt="write me an professional email"):
    openai.api_key=key
    response=openai.Completion.create(
    engine="text-davinci-003",
    prompt="write an email for"+userprompt+"without giving subject",
    temperature=0.71,
    max_tokens=100,
    frequency_penalty=0.36,
    presence_penalty=0.75
    )
    return response.get("choices")[0]['text']

# output=generate_email("write me a professional sounding email for convincing my boss for 2 days leave for my leg operation")
# print(output)