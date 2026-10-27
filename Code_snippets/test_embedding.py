import os
from dotenv import load_dotenv


from openai import OpenAI

load_dotenv()

client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

response=client.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    input="I like cars"
)

print(response.data[0].embedding)