import os
import google.generativeai as ai
import textwrap
from IPython.display import Markdown


secret_key = os.getenv('GEMNI_API')
ai.configure(api_key=secret_key)

Model = ai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=ai.GenerationConfig(
        max_output_tokens=30,
        temperature=0.5,
    ),
    system_instruction='Be concise, non-generic and start with action verbs'
)

   
async def giveSentimentDescription(context:str):
    return await Model.generate_content_async(
        f'What are the financial, economic and market implication of this news:  {context}'
    )

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

