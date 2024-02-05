import os
import openai as ai
import json


async_client = ai.AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


async def generate_description(input: str):
    messages = get_messages(input)
    print(messages)
    stream = await async_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
        temperature=0,
        max_tokens=500
    )

    all_content = ''

    print(stream)

    async for chunk in stream:
        print(chunk.choices)
        content = chunk.choices[0].delta.content

        if content:
            print(content)
            all_content += content
            yield all_content

        # yield json.dumps(chunk.model_dump(), ensure_ascii=False) + "\n"


def get_messages(input: str):
    '''
        Provide your output in json format with keys: family_member, age, medical_conditions.
        
        Family_member: mother, father, grandmother, grandfather.
        Age: age of a family member.
        medical_conditions: all chronic deseases and conditions that user will provide.
        Begin with: Let's start with some general questions. Have any of your immediate \
    family members, like parents or siblings, been diagnosed with any chronic diseases or conditions?
    '''

    delimiter = '####'
    system_message = f'''
    You are a medical assistant who helps with tracking specific medical issues. \
    Your primary goal is to get the users family member status, their age, chronic diseases or conditions \
    and when these conditions have been diagnosed.

    The user query will be delimited with {delimiter} characters.
    A user will share chronic diseases or conditions of their family members, \
    like parents or siblings. You will need to get an additional information if it was not provided \
    by asking them questions like:
    - in what age these conditions were diagnosed. \
    - if where any other conditions.
    
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
            'content': f'{delimiter}{input}{delimiter}'
            }
    )

    return messages
