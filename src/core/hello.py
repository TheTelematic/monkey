from infra.llm import llm


async def hello() -> str:
    return await llm.invoke("Hello!")
