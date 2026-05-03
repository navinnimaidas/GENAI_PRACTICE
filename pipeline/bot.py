""" Main entry point for the pipeline """
#import the packages

from .db import DatabaseConnection
from .prompts import SQL_SYSTEM_PROMPT,OUTPUT_SYSTEM_PROMPT
from .output_schema import OutputSchema
from .utils import logger

from langchain.chat_models import init_chat_model


class SqlGPT:
    def __init__(self):
        self.llm=init_chat_model(model='openai/gpt-oss-120b',model_provider='groq',temperature=0)
        self.structured_llm=self.llm.with_structured_output(OutputSchema)

        self.db_connection=DatabaseConnection()

    def get_sql_query(self,user_query:str):
        prompt=SQL_SYSTEM_PROMPT+user_query.lower().strip()
        response=self.structured_llm.invoke(prompt)
        return response
    
    def get_query_result(self,sql_query:str):
        return self.db_connection.execute_query(sql_query)
        
    def get_output(self,rows):
        output_prompt=OUTPUT_SYSTEM_PROMPT+str(rows)
        output_response=self.llm.invoke(output_prompt)
        return output_response
    
if __name__=="__main__":
    user_query="provide me city wise count of students"
    logger.info(f"User query:{user_query}")
    sql_gpt=SqlGPT()
    response=sql_gpt.get_sql_query(user_query)
    logger.info(f"Generated SQL query: {response.value}" if response.type=='QUERY' else "No query generated")
    is_executed, rows = sql_gpt.get_query_result(response)
    logger.info(f"Query result: {rows}")
    if is_executed:
        output=sql_gpt.get_output(rows)
        logger.info(f"Generated output: {output}")
        print(output)
    else:
        print("Failed to execute the query. Reason:", rows)
    

