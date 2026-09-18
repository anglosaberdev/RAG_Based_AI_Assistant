
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class Assistant:
    def __init__(
        self,
        system_prompt_str,
        llm,
        message_history=None,
        vector_store_db=None,
        employee_information=None,
    ):
        self.system_prompt_str = system_prompt_str
        self.llm = llm

        self.messages_history = message_history or []

        self.vector_store_db = vector_store_db

        self.employee_information = employee_information

        self.chain = self._get_conversation_chain()

    def get_response(self, user_input):
        response = self.chain.invoke(user_input)

        # Save conversation history
        self.messages_history.append(
            {
                "role": "human",
                "content": user_input,
            }
        )

        self.messages_history.append(
            {
                "role": "ai",
                "content": response,
            }
        )

        return response

    def greet(self, user_input):
        print(user_input)

    def _get_conversation_chain(self):

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt_str),
                MessagesPlaceholder(
                    variable_name="conversation_history"
                ),
                ("human", "{user_input}"),
            ]
        )

        output_parser = StrOutputParser()

        chain = (
            {
                "retrieved_policy_information": (
                    self.vector_store_db.as_retriever()
                    | (
                        lambda docs: "\n\n".join(
                            doc.page_content for doc in docs
                        )
                    )
                ),
                "user_input": RunnablePassthrough(),
                "conversation_history": lambda x: self.messages_history,
                "employee_information": lambda x: self.employee_information,
            }
            | prompt
            | self.llm
            | output_parser
        )

        return chain
