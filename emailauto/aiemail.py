import openai
# openai.api_key="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"
# openai.api_key="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"
# openai.api_key="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"
# openai.api_key="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" #arpitapi
openai.api_key="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" 

def generate_email(userprompt="write me an professional email"):
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