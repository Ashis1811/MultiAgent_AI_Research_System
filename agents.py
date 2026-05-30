import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url


# ── Load Environment Variables ───────────────────────────────

load_dotenv()


# ── LLM Setup ────────────────────────────────────────────────

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


# ── Simple Custom Agent Wrapper ─────────────────────────────

class SimpleAgent:

    def __init__(self, tool):
        self.tool = tool

    def invoke(self, input_data):

        user_message = input_data["messages"][-1][1]

        result = self.tool.invoke(user_message)

        return {
            "messages": [
                ("user", user_message),
                ("assistant", result)
            ]
        }


# ── Search Agent ─────────────────────────────────────────────

def build_search_agent():

    return SimpleAgent(web_search)


# ── Reader Agent ─────────────────────────────────────────────

def build_reader_agent():

    return SimpleAgent(scrape_url)




# ── Writer Chain ─────────────────────────────────────────────

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
            You are an expert research writer.

            Write:
            - clear
            - detailed
            - professional
            - structured reports
            """
                ),

                (
                    "human",

                    """
            Write a detailed research report on the topic below.

            TOPIC:
            {topic}

            RESEARCH GATHERED:
            {research}

            Structure the report as:

            - Introduction
            - Key Findings
            - Conclusion
            - Sources

            Be factual, insightful, and professional.
            """
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ── Critic Chain ─────────────────────────────────────────────

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
            You are a sharp and constructive research critic.

            Be:
            - honest
            - analytical
            - specific
            """
                ),

                (
                    "human",

                    """
            Review the research report below.

            REPORT:
            {report}

            Respond EXACTLY in this format:

            Score: X/10

            Strengths:
            - ...
            - ...

            Areas to Improve:
            - ...
            - ...

            One line verdict:
            ...
            """
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
print("critic_chain loaded")

# ── RAG QA Chain ─────────────────────────────────────────────

rag_prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
            You are a highly accurate AI document assistant.

            Rules:
            - Answer ONLY using the provided context
            - Do NOT hallucinate
            - If answer is missing, clearly say so
            - Keep answers concise and accurate
            - Use bullet points when useful
            """
    ),

    (
        "human",

        """
            QUESTION:
            {question}

            DOCUMENT CONTEXT:
            {context}
            """
    )
])

rag_chain = rag_prompt | llm | StrOutputParser()
print("rag_chain loaded successfully")