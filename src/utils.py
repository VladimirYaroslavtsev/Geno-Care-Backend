import os
import openai as ai
import json
import settings as st

async_client = ai.AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


async def generate_description(messages: list):    
    stream = await async_client.chat.completions.create(
        model='gpt-4', # gpt-3.5-turbo
        messages=messages,
        stream=True,
        temperature=0,
        max_tokens=1000,
        # response_format={ "type": "json_object" }
    )

    all_content = ''

    # print(stream)

    async for chunk in stream:
        # print(chunk.choices)
        content = chunk.choices[0].delta.content

        if content:
            # print(content)
            all_content += content
        else:
            yield all_content

        # yield json.dumps(chunk.model_dump(), ensure_ascii=False) + "\n"


def get_messages(input: str, system_message) -> list:
    '''
        Provide your output in json format with keys: family_member, age, medical_conditions.
        
        Family_member: mother, father, grandmother, grandfather.
        Age: age of a family member.
        medical_conditions: all chronic deseases and conditions that user will provide.
        Begin with: Let's start with some general questions. Have any of your immediate \
    family members, like parents or siblings, been diagnosed with any chronic diseases or conditions?
    '''

    messages = [
        {
            'role': 'system',
            'content': system_message
        }
    ]
    messages.append(
        {
            'role': 'user',
            'content': f'{st.DELIMITER}{input}{st.DELIMITER}'
        }
    )

    return messages
