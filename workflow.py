from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_groq import ChatGroq
import json


class AstroBotWorkflow:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.model = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1024,
        )
        self.workflow = self._create_workflow()
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)

    def _create_workflow(self):
        """Create the LangGraph workflow"""
        workflow = StateGraph(state_schema=MessagesState)

        # Define the function that calls the model
        def call_model(state: MessagesState):
            system_prompt = (
                "You are AstroBot, a friendly and knowledgeable space assistant. "
                "You help users learn about astronomy, space exploration, planets, stars, galaxies, and all things related to space science. "
                "Key guidelines: "
                "- Keep responses informative yet engaging "
                "- Use space-related emojis occasionally (🚀, 🌌, ⭐, 🪐, 🌙, 🛰️) "
                "- Explain complex concepts in simple terms "
                "- If asked about something not space-related, gently redirect to space topics "
                "- Keep responses concise but thorough, aiming for 2-3 sentences "
                "- Include fascinating space facts when relevant "
                "The provided chat history includes a summary of the earlier conversation."
            )

            system_message = SystemMessage(content=system_prompt)
            message_history = state["messages"][
                :-1
            ]  # exclude the most recent user input

            # Summarize the messages if the chat history reaches a certain size
            if len(message_history) >= 6:  # Summarize after 3 exchanges (6 messages)
                last_human_message = state["messages"][-1]

                # Invoke the model to generate conversation summary
                summary_prompt = (
                    "Distill the above chat messages into a single summary message about our space conversation. "
                    "Include as many specific space topics and details as you can. "
                    "Focus on what space concepts we've discussed and what the user has learned."
                )
                summary_message = self.model.invoke(
                    message_history + [HumanMessage(content=summary_prompt)]
                )

                # Delete messages that we no longer want to show up
                delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]]

                # Re-add user message
                human_message = HumanMessage(content=last_human_message.content)

                # Call the model with summary & response
                response = self.model.invoke(
                    [system_message, summary_message, human_message]
                )
                message_updates = [
                    summary_message,
                    human_message,
                    response,
                ] + delete_messages
            else:
                message_updates = self.model.invoke(
                    [system_message] + state["messages"]
                )

            return {"messages": message_updates}

        # Define the node and edge
        workflow.add_node("model", call_model)
        workflow.add_edge(START, "model")

        return workflow

    def invoke_streaming(self, user_message, session_id="default"):
        """Invoke the workflow and return streaming response"""
        try:
            # Create human message
            human_message = HumanMessage(content=user_message)

            # Configuration for this session
            config = {"configurable": {"thread_id": session_id}}

            # Invoke the workflow
            result = self.app.invoke({"messages": [human_message]}, config=config)

            # Get the last message (assistant's response)
            last_message = result["messages"][-1]
            response_content = last_message.content

            return response_content

        except Exception as e:
            raise Exception(f"Workflow error: {str(e)}")

    def clear_memory(self, session_id="default"):
        """Clear memory for a specific session"""
        try:
            # LangGraph memory clearing (if supported)
            # For now, we'll rely on the automatic summarization
            return True
        except Exception as e:
            print(f"Error clearing memory: {e}")
            return False

    def get_conversation_state(self, session_id="default"):
        """Get the current conversation state"""
        try:
            config = {"configurable": {"thread_id": session_id}}
            # This would depend on LangGraph's API for getting state
            return {"status": "active", "session_id": session_id}
        except Exception as e:
            return {"status": "error", "error": str(e)}
