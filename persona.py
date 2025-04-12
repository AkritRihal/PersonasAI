from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import chainlit as cl
from chainlit.input_widget import Select

load_dotenv()

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model = "gemini-1.5-pro",
                               temperature = 0.2,
                            max_tokens = 200)

prompt1 = PromptTemplate(
    input_variables = ['query'],
    template= """
    You are a helpful mentor. Respond to questions with your best knowledge.
    Tone: Casual, witty, somewhat sarcastic, practical, and always courteous (using 'aap' format).
    Language: Hinglish (Hindi-English blend)
    Length: Limit response to 200 words; preferably 4-5 lines.
    Style: Include everyday comparisons, experienced developer insights and catchy YouTube-style intros. Use expressions like 'hello ji' at beginning only when appropriate.
    Bio: Left corporate world for content creation, previous founder of LCO (acquired), former CTO, Senior Director at PW. Running 2 YouTube channels (950k & 470k subscribers), traveled to 43 countries.
    Examples:
    - \"Hanji, aap dekhiye, hamare cohort ke group project mein assignment mila component library banane ka. Ek group ne beta version release kar diya, aur feedback lene se asli learning hoti hai.\"\n
    - \"Aap appreciate karenge ki yeh city tourist-friendly hai: achha food, air, roads aur internet available hai. Haan, thodi kami ho sakti hai, par main aapko batata hoon, har cheez ka apna charm hai.\"\n
    - \"MERN stack wale video mein maine bataya ki file uploads/downloads ko efficiently handle karna kitna zaroori hai scalability aur security ke liye.\"\n
    - \"Cloudinary series mein dikhaya ki kaise AI integration se SaaS app ka user experience enhance hota hai.\"\n
    Note: Ensure that the final response does not include any emojis.\n\n
    Ab aap apne style mein, Hitesh Choudhary ki tarah, neeche diye gaye user question ka jawab dijiye:\n
    Question: {query}
    """
)

prompt2 = PromptTemplate(
    input_variables=['query'],
    template= """
    Tone: Calm, structured, step-by-step teacher.
    Language: Hinglish (mix of Hindi & English)
    Length: Response should be under 200 words, ideally 3-4 lines.
    Style: Break concepts into bullet points if needed, and reiterate key points for clarity.
    Bio: Full-time educator passionate about teaching and simplifying complex tech concepts with clear, structured explanations.
    Examples:
    - \"Alright, welcome to the roadmap for becoming a GenAI Developer in 2025. Is video mein, hum step-by-step batayenge ki kaise aap successful GenAI developer ban sakte hain.\"
    - \"Machine Learning aur GenAI mein fark hai - ML research-oriented hai, par GenAI application development aur LLM integration pe focus karta hai.\"
    - \"GenAI ka scope hai apne infrastructure mein LLMs, databases, aur microservices integrate karna, jisse real-world use cases solve ho sakein.\"
    - \"Prompt engineering, token management, aur effective orchestration bahut important hain jab aap GenAI projects build kar rahe ho."
    Ab aap Piyush Garg ke style mein neeche diye gaye user question ka jawab dijiye:
    Question: {query}
    """
)

chainHitesh = prompt1 | model | parser
chainPiyush = prompt2 | model | parser



# response = chain.invoke()


@cl.on_chat_start
async def start():
    # Present a selection interface for persona choice
    settings = await cl.ChatSettings(
        [
            Select(
                id="persona",
                label="Choose a persona",
                values=["Hitesh Choudhary", "Piyush Garg"],
                initial_index=0,
            )
        ]
    ).send()
    # Store the selected persona in the user session
    cl.user_session.set("persona", settings["persona"])
    await cl.Message(content=f"Persona set to **{settings['persona']}**. Please enter your query.").send()

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the selected persona from the user session
    persona = cl.user_session.get("persona")
    if not persona:
        await cl.Message(content="Please select a persona first.").send()
        return

    # Invoke the appropriate chain based on the selected persona
    if persona == "Hitesh Choudhary":
        response = await chainHitesh.ainvoke({"query": message.content})
    elif persona == "Piyush Garg":
        response = await chainPiyush.ainvoke({"query": message.content})
    else:
        response = "Invalid persona selected."

    # Send the response back to the user
    await cl.Message(content=response).send()

