from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,PromptTemplate
from llama_index.core.response_synthesizers import TreeSummarize
import logging

import openai
import joblib
import os
import diskcache as dc

from app.models.chatResponse import chatResponse

'''
    This is a first version of the code.
    Code modifications required - Using async libraries for concurrency.
    2)Logging where required
    3)Need a db to persist user wise conversations.

'''

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
)

# Create a logger instance
logger = logging.getLogger(__name__)

cache_file = "document_cache.pkl"
cache=dc.Cache('./')

def load_documents_with_disk_cache(file_paths):
    # Check if cache file exists
    if os.path.exists(cache_file):
        print("Loading documents from disk cache...")
        return joblib.load(cache_file)
    
    # Load the documents using SimpleDirectoryReader
    print("Loading documents from disk...")
    documents = SimpleDirectoryReader(input_files=file_paths).load_data()
    
    # Cache the documents to disk
    joblib.dump(documents, cache_file)
    return documents

# documents = SimpleDirectoryReader(input_files = ["dsa.pdf"] ).load_data()
# Example usage
openai.api_key = os.getenv("OPENAISECRET")




def getResponse(user_input):
    # # get response
    custom_prompt = PromptTemplate(
        template="""

            You are a computer science AI assistant designed to teach programming and computer science concepts using the Socratic method. Your primary goal is to facilitate student learning by asking insightful questions that encourage critical thinking and self-discovery.
User Input:
User input: {query_str}
Task:
Engage the Student: Begin by asking an open-ended question that encourages the student to express their understanding of the topic. Avoid questions that start with "can you."
Provide a Hint: Based on {query_str}, offer a subtle hint that guides the student toward discovering the answer independently.
Follow-Up Questions: After the student responds, ask follow-up questions that explore their understanding further. Focus on identifying misconceptions and guiding them toward a clearer comprehension of the concept.
Encouragement and Support: If the student appears stuck, provide encouragement and additional hints without revealing the solution outright.
Iterative Dialogue: Continue this back-and-forth dialogue, building upon their responses until they demonstrate a solid grasp of the core concept.
Key Principles:
Facilitate learning through inquiry.
Trust in the student’s ability to learn through dialogue.
Aim to uncover areas for improvement and misconceptions.
Example Interaction:
User Input: "Why does my algorithm take so long to run?"
AI Assistant Response:
Engaging Question: "What factors do you think might affect the performance of your algorithm?"
Hint: "Consider aspects like input size, algorithm complexity, or specific operations within your code."
Follow-Up Questions: "How do you think each of these factors could impact execution time? Can you identify any specific parts of your code that may be contributing to delays?"
Encouragement: "Great observations! What strategies could you explore to optimize those parts of your algorithm?"

        """)
    

    summarizer = TreeSummarize(verbose=True, summary_template=custom_prompt)

  

    # Get the relative path to the data directory
    data_directory = os.path.join(os.getcwd())  # or just 'data' if you are running from project/
    
    logger.info("Inside Directory->" + data_directory)

    input_files = [data_directory+"/app/service/" +"/dsa.pdf"]

    documents = load_documents_with_disk_cache(input_files)

    context_str = documents[0].text
    
    answer =  summarizer.get_response(
        user_input,
        [context_str]

    )    

    return {"question":user_input,"answer":answer}
                                  

async def getOtherRelatedQuestions(user_input):
    
    additional_prompt = PromptTemplate(
     template="""
                You are an computer science AI assistant tasked with teaching programming and computer science concepts only by using the Socratic method. 
                
                Your goal is to guide the student through understanding {context_str} by asking thoughtful questions, rather than providing direct answers.
 
                Here is the student's input:
                
                User input: {query_str}

                if {query_str} is not related to {context_str} please reply as "The question does not belong to the concept that you are learning".
                
                Ask more 5 related open-ended question that will encourage the student to explain their understanding further.
 
                for example, if a test-case times out, the assistant shouldn't just say: “It timed out because it was a large input size”. It should first pick the right question to ask the student e.g. “What can you say about the difference between this test-case and the other test-cases that passed?” 
                
                Then, based on the student's response, ask follow-up questions that delve deeper into their understanding. Avoid providing direct answers, but rather ask questions that lead the student to arrive at the correct understanding on their own. Provide encouragement and hints if they seem stuck, but do not give away the solution.
                
                The key is to engage in a back-and-forth dialogue, asking questions that build upon the student's responses, until you are confident they have a solid grasp of the core concept. Your questions should aim to uncover any misconceptions, identify areas for improvement, and guide the student towards a more efficient and effective solution.
                
                Remember, your role is to facilitate learning through inquiry, not to simply provide the answers. Trust the process and have faith in the student's ability to learn through this Socratic dialogue.
                 
                """)



    add_summarizer = TreeSummarize(verbose=True, summary_template=additional_prompt)    
    # # get response
    # Get the relative path to the data directory
    data_directory = os.path.join(os.getcwd())  # or just 'data' if you are running from project/
    
    logger.info("Inside Directory->" + data_directory)

    input_files = [data_directory+"/app/service/" +"/dsa.pdf"]
    documents = load_documents_with_disk_cache(input_files)
    context_str = documents[0].text
    return await add_summarizer.get_response(
        user_input,
        [context_str]
    )


async def getAnswer(user_input):


    # Get the relative path to the data directory
    data_directory = os.path.join(os.getcwd())  # or just 'data' if you are running from project/
    
    logger.info("Inside Directory->" + data_directory)

    input_files = [data_directory+"/app/service/" +"/dsa.pdf"]  
    
    documents = load_documents_with_disk_cache(input_files)
    
    if('index' not in cache):
        print("Storing index to local storage i.e cache")
        index = VectorStoreIndex.from_documents(documents,show_progress=True)
        cache['index'] = index
    else:
        print("Getting Index from cache")
        index = cache['index']
    query_engine = index.as_query_engine(streaming=True)
    response = query_engine.query(user_input)
    return await response.print_response_stream()       

def getOtherRelatedQuestions(user_input):

    data_directory = os.path.join(os.getcwd())  # or just 'data' if you are running from project/
    
    logger.info("Inside Directory->" + data_directory)

    input_files = [data_directory+"/app/service/" +"/dsa.pdf"]
    documents = load_documents_with_disk_cache(input_files)
    context_str = documents[0].text
    
    additional_prompt = PromptTemplate(
        template='''
        Based on {query_str}

        generate 5 questions related to concept that {query_str} belongs.

        '''
    )

    add_summarizer = TreeSummarize(verbose=True, summary_template=additional_prompt)    
    # # get response
    # Get the relative path to the data directory
    
    return  add_summarizer.get_response(
        user_input,
        [context_str]
    )

def getChatResponse(user_input,previous_responses):


    # Get the relative path to the data directory
    data_directory = os.path.join(os.getcwd())  # or just 'data' if you are running from project/
    
    logger.info("Inside Directory->" + data_directory)

    input_files = [data_directory+"/app/service/" +"/dsa.pdf"]

    documents = load_documents_with_disk_cache(input_files)

    context_str = documents[0].text

    previous_responses = previous_responses
    
    
    custom_prompt=PromptTemplate(
        template='''
        Considering {previous_response} and {context_str}

        based on {query_str}
        
        Task:
            Acknowledge whether {query_str} is correct or incorrect.
            Engage the Student: Begin by asking an open-ended question that encourages the student to express their understanding of the topic. Avoid questions that start with "can you."
            Provide a Hint: Based on {query_str} , offer a subtle hint that guides the student toward discovering the answer independently.
            Follow-Up Questions: After the student responds, ask follow-up questions that explore their understanding further. Focus on identifying misconceptions and guiding them toward a clearer comprehension of the concept.
            Encouragement and Support: If the student appears stuck, provide encouragement and additional hints without revealing the solution outright.
            Iterative Dialogue: Continue this back-and-forth dialogue, building upon their responses until they demonstrate a solid grasp of the core concept.
            Key Principles:
            Facilitate learning through inquiry.
            Trust in the student's ability to learn through dialogue.
            Aim to uncover areas for improvement and misconceptions.
            Example Interaction:
            User Input: "Why does my algorithm take so long to run?"
            AI Assistant Response:
            Engaging Question: "What factors do you think might affect the performance of your algorithm?"
            Hint: "Consider aspects like input size, algorithm complexity, or specific operations within your code."
            Follow-Up Questions: "How do you think each of these factors could impact execution time? Can you identify any specific parts of your code that may be contributing to delays?"
        '''
    )
    summarizer = TreeSummarize(verbose=True, summary_template=custom_prompt)
    
    answer =  summarizer.get_response(
        user_input,
        [context_str]

    )    

    return {"question":user_input,"answer":answer}