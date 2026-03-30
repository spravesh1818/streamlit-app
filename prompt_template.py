from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableParallel
load_dotenv()

model=ChatOpenAI(model="gpt-4o-mini")
draft_email_prompt_template=PromptTemplate(
    template="""
    You are a helpful email assisant.Your task is to write a draft email for the following email.
    Topic: {email_topic}
    Recipient: {recipient}
    Name: {name}
    
    Give me the draft email in the following json format:
    {{
        "draft_email": "This is the draft email"
    }}
    """
)

draft_email_chain=draft_email_prompt_template|model|JsonOutputParser()

grammar_chain_prompt_template=PromptTemplate(
    template="""
    You are a helpful email assisant.Check and validate the grammar of the following email.
    Email: {draft_email}
    Also humanize the email to make it more natural and readable.
    Give me the grammar in the following json format:
    {{
        "grammar_check_complete": "This is the grammar check",
        "final_email": "This is the humanized email"
    }}
    """
)

grammar_chain=grammar_chain_prompt_template|model|JsonOutputParser()

combined_chain=(draft_email_chain|grammar_chain)

subject_line_prompt=PromptTemplate(
    template="""
    You are a helpful email assisant.Generate a subject line for the following email.
    question: {question}

    Give me the subject line in the following json format:
    {{
        "subject_line": "This is the subject line"
    }}
    """
)

subject_line_chain=subject_line_prompt|model|JsonOutputParser()

parallel_chain=RunnableParallel(
    {
        "combined_chain": combined_chain,
        "subject_line": subject_line_chain,
    }
)


