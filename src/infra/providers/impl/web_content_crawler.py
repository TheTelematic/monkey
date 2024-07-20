from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.docstore.document import Document
from langchain_community.utilities import ApifyWrapper
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

import config
from infra.providers.base import ProviderBase


class ApifyContentCrawler(ProviderBase):
    CONTENT_URL = config.APIFY_CONTENT_CRAWLER_URL
    LLM_MODEL = "gpt-4o"

    def __init__(self):
        self._check_config()

        self._embedding = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        self._index = VectorStoreIndexWrapper(
            vectorstore=PineconeVectorStore(embedding=self._embedding, **self.pinecone_vectorstore_kwargs())
        )

    @staticmethod
    def _check_config():
        if not config.APIFY_API_TOKEN:
            raise ValueError("APIFY_API_TOKEN is not set in the config.")

        if not config.APIFY_CONTENT_CRAWLER_URL:
            raise ValueError("APIFY_CONTENT_CRAWLER_URL is not set in the config.")

        if not config.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set in the config.")

        if not config.PINECONE_INDEX_NAME:
            raise ValueError("PINECONE_INDEX_NAME is not set in the config.")

        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the config.")

    @staticmethod
    def pinecone_vectorstore_kwargs() -> dict:
        return {
            "pinecone_api_key": config.PINECONE_API_KEY,
            "index_name": config.PINECONE_INDEX_NAME,
        }

    async def load_data(self):
        loader = await ApifyWrapper(APIFY_API_TOKEN=config.APIFY_API_TOKEN).acall_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": [{"url": self.CONTENT_URL}]},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )

        # Create a vector store based on the crawled data
        creator = VectorstoreIndexCreator(
            vectorstore_cls=PineconeVectorStore,
            embedding=self._embedding,
            vectorstore_kwargs={
                "pinecone_api_key": config.PINECONE_API_KEY,
                "index_name": config.PINECONE_INDEX_NAME,
            },
        )
        await creator.afrom_loaders([loader])

    async def invoke(self, text: str) -> str:
        return await self._index.aquery(
            text, llm=ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model=self.LLM_MODEL)
        )


apify = ApifyContentCrawler()
