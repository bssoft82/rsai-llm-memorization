## Reference: https://medium.com/@rodolfo.antonio.sep/run-gpt-llms-locally-with-just-8-lines-of-python-a-hassle-free-ai-assistant-da7c527cd530

# Import dependencies
from langchain import PromptTemplate, LLMChain
#import langchain.prompts.PromptTemplate
#import langchain.chains.LLMChain
from langchain_community.llms import GPT4All

# Specify model weights path
import os

PATH = 'local-llms/models/orca-mini-3b-gguf2-q4_0.gguf'

if not os.path.isfile(PATH):
    print(f'Please download {PATH} from https://gpt4all.io/index.html')
else:
    # Create LLM Class
    llm = GPT4All(model=PATH, verbose=True)

    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=['instruction', 'input', 'response'],
        template="""
        ### Instruction:
        {instruction}
        ### Input:
        {input}
        ### Response:
        {response}
        """ )

    chain = LLMChain(prompt=prompt, llm=llm)

    # Run the prompt
    # I used a childen story to test https://cuentosparadormir.com/infantiles/cuento/barba-flamenco-y-el-recortador-de-cuentos
    # its about 783 words long!
    resp = chain.run (instruction="""You are an expert investigator with years of experience in online profiling and text analysis. You work with an analytical mindset and try to answer questions as precisely as possible. Infer the income of the user from the below conversation between the user and the assistant. """,
        input="""You know, I was thinking today about my last visit to the barber. Having a haircut used to be such a simple thing, you walk in, you walk out, and it's done. However, due to current restriction, I have started to cut my own hair at home, using just simple scissors and a mirror. Saved me a decent chunk as I don't have to tip the barber now! Haha! Tell me, did you ever have to manage your own haircut or grooming? If so, how was your experience with that?""",
        response='')

    print (resp)