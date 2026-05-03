
from pipeline.bot import SqlGPT
from pipeline.utils import logger

class Botendpoint:
    def __init__(self):
        self.sql_gpt=SqlGPT()

    async def get_response(self,user_query:str):
        
        logger.info("********SQL GPT initialized **************")
        logger.info("********QUERY CREATION PIPELINE STARTED **************")
        response=self.sql_gpt.get_sql_query(user_query)
        logger.info("********QUERY CREATION PIPELINE COMPLETED **************")

        if response.type=='QUERY':
            logger.info("********QUERY EXECUTION STARTED **************")
            status,query_result=self.sql_gpt.get_query_result(response.value)

            if status:
                logger.info("********FINAL RESULT PREPERATION STARTED **************")
                return self.sql_gpt.get_output(query_result).content
            else:
                return "Something went wring! please contact your IT suuport team"
        else:
            return response.value



