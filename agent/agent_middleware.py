from langchain.agents.middleware import before_model, wrap_tool_call, dynamic_prompt
from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompt, load_report_prompts\

# 调用模型前
@before_model
def before_model_logger(agent_state,runtime):
    logger.info(f"[log_before_model]即将调用模型，带有{len(agent_state['messages'])}条消息。")
    logger.debug(f"[log_before_model]{type(agent_state['messages'][-1]).__name__}: {agent_state['messages'][-1].content.strip()}")
    return None

# 调用工具时执行
@wrap_tool_call
def wrap_tool_call(request, handler):
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True  # 让标记“report” = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e

# 调用提示词前执行
@dynamic_prompt
def dynamic_prompt(request):
    is_report = request.runtime.context.get('report', False)    # 获取标记“report”, 默认返回False
    if is_report:
        return load_report_prompts()
    return load_system_prompt()