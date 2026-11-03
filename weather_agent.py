from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tool_list import tool_list
# 构建模型
def load_model():
    model = ChatOllama(model="qwen3.5:4b", base_url="http://127.0.0.1:11434")
    return model



def get_agent(model, tool_list, system_prompt):
    return create_agent(model=model, tools=tool_list,system_prompt=system_prompt, checkpointer=MemorySaver())

def main():
    model = load_model()
    tools = tool_list()
    system_prompt = "你是一个天气助手，请根据用户的问题查询实时天气并提出一些生活建议"
    agent = get_agent(model, tools, system_prompt)
    while True:
        user_input = input("请输入问题：")
        if user_input == "bye":
            break
        result = agent.invoke(
            {"messages": [{"role": "user","content": user_input}]},
            config={"configurable": {"thread_id": "user_001"}} 
            )
        anser = result['messages'][-1].content
        print(anser)
        
if __name__ == "__main__":
    main()