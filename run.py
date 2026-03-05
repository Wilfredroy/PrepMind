from google import genai
client = genai.Client(api_key="AIzaSyADKhX9bFfWWJ7XiArGr7ezSwRGww1mvPY")
for m in client.models.list():
    print(m.name)