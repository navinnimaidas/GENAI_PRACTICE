""" Main entry point for the pipeline """
#import the packages

from db import DatabaseConnection
from prompts import SQL_SYSTEM_PROMPT,OUTPUT_SYSTEM_PROMPT
from output_schema import OutputSchema

from langchain.chat_models import init_chat_model
llm=init_chat_model(model='openai/gpt-oss-120b',model_provider='groq',temperature=0)
structured_llm=llm.with_structured_output(OutputSchema)

class SqlGPT:
    def get_sql_query(self,user_query:str):
        prompt=SQL_SYSTEM_PROMPT+user_query.lower().strip()
        response=structured_llm.invoke(prompt)
        return response
    
    def get_query_result(self,response):
        if response.type=='QUERY':
            db=DatabaseConnection()
            is_success,connection=db.get_connection()
            if is_success:
                is_executed, rows = db.execute_query(connection,response.value)
                connection.close()
                return is_executed, rows
            else:
                return False, connection
        else:
            return False, "Response type is not QUERY"
        
    def get_output(self,rows):
        output_prompt=OUTPUT_SYSTEM_PROMPT+str(rows)
        output_response=llm.invoke(output_prompt)
        return output_response.content
    

