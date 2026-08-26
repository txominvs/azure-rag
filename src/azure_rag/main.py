import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from openai import OpenAI

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

from fastapi import FastAPI

load_dotenv()

credential = DefaultAzureCredential()

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    ),
)

search = SearchClient(
    os.environ["AZURE_SEARCH_ENDPOINT"],
    os.environ["AZURE_SEARCH_INDEX"],
    credential,
)

def rag(question: str):
    docs = search.search(
        search_text=question,  # BM25
        vector_queries=[
            VectorizableTextQuery(
                text=question,
                fields="contentVector",
                k_nearest_neighbors=3,
            )
        ],
        top=3,
    )
    
    context = "\n".join(d["content"] for d in docs)

    response = client.responses.create(
        model=os.environ["AZURE_OPENAI_MODEL"],
        input=f"""Answer only from the context.
    {context}

    Question: {question}""",
    )

    return {"answer": response.output_text}


app = FastAPI()
@app.post("/ask")
def ask(question):
    return rag(question)