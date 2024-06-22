from langchain_openai import OpenAIEmbeddings


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small" 

""" 
An embdding is a sequence of numbers that represents the concepts within content. Embeddings make it easy for machine learning models
and other algorithms to understand the relationships between content and to perform tasks like retrieval.

Source: https://openai.com/index/new-embedding-models-and-api-updates/

Pricing for text-embedding-3-small has reduced by 5X compared to text-embedding-ada-002, from a price per 1k tokens of $0.0001 to $0.00002.
"""
class Memory:
    def __init__(self, embedding_provider, **kwargs):
        _embeddings = None
        match embedding_provider:
            case "openai":
                _embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
            case "huggingface":
                from langchain_community.embeddings import HuggingFaceEmbeddings
                _embeddings = HuggingFaceEmbeddings()
            case _:
                raise Exception("Embdding provider not found.")
            
        self._embeddings = _embeddings
                
    def get_embeddings(self):
        return self._embeddings