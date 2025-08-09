from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt template
system_prompt = (
    "You are a helpful assistant and you are a pro level expert in the {domain} domain. "
    "Please respond to the user queries."
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

def generate_response(message_history, api_key, llm, temperature, max_tokens, domain):
    chat_llm = ChatOpenAI(
        openai_api_key=api_key,
        model=llm,
        temperature=temperature,
        max_tokens=max_tokens
    )
    parser = StrOutputParser()

    if not message_history or message_history[-1]["role"] != "user":
        raise ValueError("Latest message in history must be from the user.")

    history = message_history[:-1] if len(message_history) > 1 else []
    latest_input = message_history[-1]["content"]

    chain = prompt | chat_llm | parser
    answer = chain.invoke({
        "history": history,
        "input": latest_input,
        "domain": domain
    })
    return answer