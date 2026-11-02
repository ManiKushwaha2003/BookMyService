from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
import chromadb
from apps.chat.tool import get_service
from langchain_core.messages import ToolMessage


load_dotenv()

loader = TextLoader(
    "apps/chat/knowledge.txt",
    encoding="utf-8"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="bookmyservice_knowledge"
)

texts = [chunk.page_content for chunk in chunks]
embeddings = model.encode(texts).tolist()

collection.upsert(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=texts,
    embeddings=embeddings
)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)


tools = [get_service]

llm_with_tools = llm.bind_tools(tools)

tool_map = {t.name: t for t in tools}



prompt = ChatPromptTemplate.from_template(
    """
    You are the BookMyService Assistant, the official AI assistant
    for the BookMyService platform.

    Your purpose is to help users understand services, bookings,
    provider offers, booking statuses, ratings, and platform features.

    User Question:
    {question}

    Retrieved Context:
    {context}

    Rules:
    - If the user asks who you are, introduce yourself as the
      BookMyService Assistant.
    - Give short and simple answers in easy English.  
    - If the user greets you, respond politely.
    - Use bullet points only when needed.
    - If asked who you are, introduce yourself as BookMyService Assistant.
    - Use the retrieved context for project-related questions.
    - Avoid complex words and unnecessary details.
    - For project-related questions, use the retrieved context.
    - If the context does not contain the answer, say that the
      information is not available in the knowledge base.
    - Never invent booking statuses, prices, offers, or ratings.
    - Never claim to perform an action without API confirmation.
    - Answer only what the user asks.
    - Stay focused on BookMyService and its features.
    - Be polite, helpful, and consistent.
    - Use bullet points only when needed.
    - Do not repeat the question in your answer.
    - Do not provide code unless the user asks for code.    

    - If a question is unclear, ask one short clarification question.
    - If the user asks how to do something, provide simple steps.
    - If the user asks for a comparison, explain the key differences briefly.
    - If the user asks for a definition, explain it in easy words.
    - If the user asks for code, provide correct and simple code.
    - Explain technical terms only when necessary.
    - Do not repeat the retrieved context word for word unless needed.
    - Ignore irrelevant context and use only information related to the question.
    - If the context contains conflicting information, do not guess;
      explain that the information is unclear.
    - Do not pretend to access live bookings, user accounts, or provider
      details unless the required API or tool provides that information.
    - Do not say an API action succeeded if it failed or its result is unknown.
    - Keep every answer focused on BookMyService whenever relevant.
    - For unrelated questions, respond briefly when appropriate and
      politely guide the user back to BookMyService.
    - Do not include unnecessary introductions, conclusions, or disclaimers.
    - Answer in the same language as the user when possible.
    - Maintain a consistent and easy-to-understand response style.

- If the user asks how to do something, explain the process
  step by step using simple, numbered steps.
- Keep each step short and clear.
- Provide only the steps needed to complete the task.
- For simple questions, give a direct answer instead of steps.



- Answer only using the retrieved RAG context.
- Do not use external knowledge or make assumptions.
- If the answer is not available in the retrieved context, say:
  "Sorry, this information is not available in our knowledge base."

- If the user asks about available services, call the
  get_service tool to fetch the latest data from the database.
- Use the database tool result for available service questions.
- Do not invent service names.


    """
)

chain = prompt | llm | StrOutputParser()


def get_chatbot_response(question):
    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    documents = results.get("documents") or [[]]
    context = "\n".join(documents[0])

    messages = prompt.invoke({
        "question": question,
        "context": context
    }).to_messages()

    response = llm_with_tools.invoke(messages)

    while response.tool_calls:
        messages.append(response)

        for tool_call in response.tool_calls:
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

        response = llm_with_tools.invoke(messages)

    return response.content
