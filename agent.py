from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import AgentType, initialize_agent
from langchain.prompts.prompt import PromptTemplate
from langchain import hub
from tools.cypher import cypher_qa
from langchain.tools import Tool
from tools.vector import kg_qa
from llm import llm

tools = [
    Tool.from_function(
        name="Graph Cypher QA Chain",
        description="Berikan informasi mengenai permasalahan fikih termasuk bab, pembahasan, mazhab, dan pendapat",
        func = cypher_qa,
       # return_direct=True
    )
]

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)

SYSTEM_MESSAGE = """
Anda adalah seorang pakar taharah perbedaan fikih empat mazhab yaitu, Syafii, Maliki, Hambali, dan Hanafi yang dapat memberikan jawaban mengenai permasalahan fikih kepada masyarakat.
Jawablah pertanyaan berikut sebaik mungkin.
Jangan menjawab pertanyaan yang tidak terkait dengan bab fikih, pembahasan, mazhab, dan pendapat hukum.

Jangan jawab pertanyaan apa pun menggunakan pre-trained knowledge Anda, hanya gunakan informasi yang disediakan dalam knowledge base pada Neo4j.
"""

agent = initialize_agent(
    tools,
    llm,
    memory=memory,
    verbose=True,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    agent_kwargs= {"system_message" : SYSTEM_MESSAGE}
)


def generate_response(prompt):
    response = agent(prompt)

    return response['output']