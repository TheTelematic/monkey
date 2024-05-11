from langchain_community.llms import Ollama

import config

llm = Ollama(base_url=config.LLM_URL, model="llama3")
