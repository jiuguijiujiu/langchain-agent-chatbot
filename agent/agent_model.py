from langchain.agents import create_agent
from utils.model_factory import chat_model
from agent.agent_tool import (rag, get_weather, get_user_location, get_user_id,
                                    get_current_month, fetch_external_data, fill_context_for_report)
from utils.prompt_loader import load_system_prompt
from agent.agent_middleware import before_model_logger, wrap_tool_call, dynamic_prompt

class Agent:
    def __init__(self):
        # 创建agent对象
        self.agent = create_agent(
            model = chat_model,
            tools = [rag, get_weather, get_user_location, get_user_id,
                    get_current_month, fetch_external_data, fill_context_for_report],
            system_prompt = load_system_prompt(),
            middleware = [before_model_logger, wrap_tool_call, dynamic_prompt]
        )

    # 接收问题，返回ai回复结果
    def stream_output(self, query):
        input_dict = {
            'messages': [
                {'role': 'user', 'content': query}
            ]
        }
        # 调用agent对象，并且创建标记'report'
        for chunk in self.agent.stream(input=input_dict, stream_mode="values", context={'report': False}):
            latest_message = chunk['messages'][-1]
            if latest_message.content:
                yield latest_message.content.strip() + '\n'

if __name__ == '__main__':
    agent = Agent()

    for chunk in agent.stream_output("给我生成我的使用报告"):
        print(chunk, end="", flush=True)