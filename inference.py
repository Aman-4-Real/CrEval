'''
Author: Aman
Date: 2025-09-01 17:47:36
Contact: cq335955781@gmail.com
LastEditors: Aman
LastEditTime: 2025-09-02 14:56:53
'''
import os
from openai import OpenAI



# ===== Given Prompt =====
SYSTEM_PROMPT = (
    "你是一个语言创意评估专家。我会给你一条指令和对应的两个回复，"
    "请对两个回复的创意程度进行评估。下面是具体的数据："
)


def build_user_prompt(query: str, resp1: str, resp2: str) -> str:
    """
    按要求拼接输入格式（必须严格保持这些标记与文案）
    """
    return (
        "[[DATA FIELD START]]\n"
        "### Query:\n" f"{query}\n"
        "### Response 1:\n" f"{resp1}\n"
        "### Response 2:\n" f"{resp2}\n"
        "[[DATA FIELD END]]\n"
        "请注意：1.挖掘创意的核心内涵，即对指令有用且新颖的回复；"
        "2.仔细比较和评估上述两个回复的创意程度，并以“更有创意的回复是：Response ”或"
        "“二者的创意程度相当。”的形式作为结尾给出你的评估决定。"
    )


def infer_once(system_prompt: str, user_prompt: str) -> str:
    """
    Inference once.
    """
    client = OpenAI(api_key="0", base_url="http://0.0.0.0:8000/v1") # this is fixed (see llamafactory)
    resp = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct", # this is fixed (see llamafactory)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=16,
    )
    return resp.choices[0].message.content


def translate_creativity_output(output: str) -> str:
    """
    Turn output into English.
    """
    output = output.strip()
    if "二者的创意程度相当" in output:
        return "After careful evaluation, I think the creativity of both responses is comparable."
    elif "更有创意的回复是：Response 1" in output:
        return "After careful evaluation, I think the more creative response is: Response 1"
    elif "更有创意的回复是：Response 2" in output:
        return "After careful evaluation, I think the more creative response is: Response 2"
    else:
        return "Unknown output format."


def main():
    print("🚀 Welcome to CrEval! (enter 'exit' anytime to quit)")
    while True:
        query = input("\n[User] Query: ").strip()
        if query.lower() == "exit":
            break
        r1 = input("[User] Response 1: ").strip()
        if r1.lower() == "exit":
            break
        r2 = input("[User] Response 2: ").strip()
        if r2.lower() == "exit":
            break
        
        user_prompt = build_user_prompt(query, r1, r2)
        try:
            output = infer_once(SYSTEM_PROMPT, user_prompt)
            print("\n[CrEval result]:\n")
            print(translate_creativity_output(output))
            print("\n"+"-"*20)
        except Exception as e:
            print("[Error]", e)

    print("👋 Exit.")

if __name__ == "__main__":
    main()



