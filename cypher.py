from langchain.prompts.prompt import PromptTemplate
from langchain.chains import GraphCypherQAChain

from llm import llm
from graph import graph

CYPHER_GENERATION_TEMPLATE = """
Anda adalah seorang pakar Pengembang Neo4j yang dapat menerjemahkan pertanyaan pengguna ke dalam kueri Cypher untuk menjawab pertanyaan taharah berdasarkan empat mazhab yaitu, Syafii, Maliki, Hambali, dan Hanafi dalam bahasa Indonesia.
Semua data yang tersedia bersumber dari kitab Rahmatul Ummah Fii Ikhtilaf Al-Aimmah karya Muhammad bin Abdurrahman As-Syafii Ad-Dimaski
Konversi pertanyaan pengguna berdasarkan skema graf.

Jika tidak ada konteks yang dikembalikan, jangan mencoba menjawab pertanyaan tersebut.
Jangan gunakan jenis relationship atau node apa pun yang tidak tersedia dalam basis data.
Jawab pertanyaan sesuai dengan basis data, jangan menjawab berdasarkan sumber lain.

Example Cypher Statements:
```
1. Mengacu pada Pembahasan

MATCH (p:Pembahasan)-[:BELIEVES]->(h:Pendapat)-[:ACCORDING_TO]->(m:Mazhab)
WHERE p.pembahasan = "kewajiban istinja"
RETURN h.hukum, m.mazhab

2. Memahami konteks dengan mengacu pada Bab

MATCH (b:Bab)-[:DISCUSSES]->(p:Pembahasan)-[:BELIEVES]->(h:Pendapat)-[:ACCORDING_TO]->(m:Mazhab)
WHERE toLower(b.bab) = "wudu" AND p.pembahasan = "mengusap leher"
RETURN h.hukum, m.mazhab
```

Schema:
{schema}

Question: 
{question}
"""

cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_prompt
)

def generate_response(prompt):

    response = cypher_qa.run(prompt)

    return response