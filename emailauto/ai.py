import requests

url = "https://openai80.p.rapidapi.com/completions"

payload = {
	"model": "text-davinci-003",
	"prompt": "Say this is a test",
	"max_tokens": 7,
	"temperature": 0,
	"top_p": 1,
	"n": 1,
	"stream": False,
	"logprobs": None,
	"stop": ""
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "166c66ffd2msh2e4d14eed209c18p1ac09ajsnf4a13f85f57c",
	"X-RapidAPI-Host": "openai80.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())