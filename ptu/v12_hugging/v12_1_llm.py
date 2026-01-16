# 

import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="auto"
)

# 사용자 질문 입력 받기
answer = input("질문을 입력해주세요. : ")

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3.2:novita",
    messages=[
        {
            "role": "user",
            "content": answer
        }
    ],
)

# 답변 출력
print(completion.choices[0].message)