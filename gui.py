
import streamlit as st


class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages_history
        self.employee_information = assistant.employee_information

    def get_response(self, user_input):
        response = self.assistant.get_response(user_input)

        if not isinstance(response, str):
            response = str(response)

        return response

    def render_messages(self):
        for message in self.messages:
            if message["role"] == "human":
                st.chat_message("human").markdown(message["content"])

            elif message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def render_user_input(self):
        user_input = st.chat_input("Type here...", key="input")

        if user_input:
            # User message
            st.chat_message("human").markdown(user_input)

            # Get AI response
            response = self.get_response(user_input)

            # AI message
            with st.chat_message("ai"):
                st.markdown(response)

            st.session_state["messages"] = self.messages

    def render(self):
        with st.sidebar:
            st.logo(
                "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg"
            )

            st.title("Umbrella Corporation Assistant")

            st.subheader("Employee Information")
            st.json(self.employee_information)

        self.render_messages()
        self.render_user_input()
