import asyncio
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "Falta OPENAI_API_KEY. Copiá .env.example a .env y completá tu key."
    )

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    temperature=0,
)
parser = StrOutputParser()

tech = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en tecnologías innovadoras de {topic}."),
    ("human", "¿Qué tecnología crees que es la más innovadora? "
              "Responde solo con su nombre, sin explicación."),
]) | model | parser

advice = ChatPromptTemplate.from_messages([
    ("human", "Explícame los beneficios de {subtopic} en 3 puntos."),
])

tech_chain = tech | (lambda nombre: {"subtopic": nombre}) | advice | model | parser


async def main() -> None:
    resultado = await tech_chain.ainvoke({"topic": "biotecnología"})
    print(resultado)


if __name__ == "__main__":
    asyncio.run(main())