import os
from dotenv import load_dotenv

from openai import OpenAI

import numpy as np

load_dotenv()

client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    response=client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )

    return response.data[0].embedding

def cosine_similarity(a,b):
    dp=np.dot(a,b)
    lena=np.linalg.norm(a)
    lenb=np.linalg.norm(b)
    return dp/(lena*lenb)

t1="Python is a programming language"
t2="An example of coding language is python"
t3="I love cars"

e1=get_embedding(t1)
e2=get_embedding(t2)
e3=get_embedding(t3)

s1=cosine_similarity(e1,e2)
s2=cosine_similarity(e1,e3)

print(s1)
print(s2)


