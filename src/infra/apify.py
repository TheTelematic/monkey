from langchain.indexes import VectorstoreIndexCreator
from langchain_community.docstore.document import Document
from langchain_community.utilities import ApifyWrapper
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

import config
from infra.llms.base import LLMBase


class ApifyContentCrawler(LLMBase):
    CONTENT_URL = config.APIFY_CONTENT_CRAWLER_URL
    LLM_MODEL = "gpt-4o"

    def __init__(self):
        if not config.APIFY_API_TOKEN:
            raise ValueError("APIFY_API_TOKEN is not set in the config.")

        if not config.APIFY_CONTENT_CRAWLER_URL:
            raise ValueError("APIFY_CONTENT_CRAWLER_URL is not set in the config.")

        self.wrapper = ApifyWrapper(APIFY_API_TOKEN=config.APIFY_API_TOKEN)

    async def invoke(self, text: str) -> str:
        loader = await self.wrapper.acall_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": [{"url": self.CONTENT_URL}]},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )

        # Create a vector store based on the crawled data
        embedding = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        creator = VectorstoreIndexCreator(
            vectorstore_cls=PineconeVectorStore,
            embedding=embedding,
            vectorstore_kwargs={
                "pinecone_api_key": config.PINECONE_API_KEY,
                "index_name": config.PINECONE_INDEX_NAME,
            },
        )
        index = await creator.afrom_loaders([loader])

        # Query the vector store
        return await index.aquery(text, llm=ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model=self.LLM_MODEL))


apify = ApifyContentCrawler()
