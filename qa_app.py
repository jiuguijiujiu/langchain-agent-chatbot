import streamlit as st
from agent.agent_model import Agent
import time

st.title(body='客服')
st.divider()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 循环输出消息聊天界面，防止消失
for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])

if 'agent' not in st.session_state:
    st.session_state['agent'] = Agent()

# 用户输入框
query = st.chat_input()

if query:
    st.chat_message('user').write(query)
    st.session_state['messages'].append({'role': 'user', 'content': query})

    ai_res_list = []
    def capture(generator, cache_list):
        for message in generator:
            cache_list.append(message)
            for char in message:
                time.sleep(0.01)
                yield char

    with st.spinner(text='模型思考中...'):
        # stream_output方法调用Agent对象，返回ai回复
        res = st.session_state['agent'].stream_output(query)
        st.chat_message('assistant').write_stream(capture(res, ai_res_list))
        content = ''.join(ai_res_list)
        st.session_state['messages'].append({'role': 'assistant', 'content': content})
        # 重跑脚本
        st.rerun()


