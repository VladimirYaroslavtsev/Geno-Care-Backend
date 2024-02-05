import os

VERSION = '0.0.1'

URI = os.environ.get('URI', 'neo4j://0.0.0.0:7474')
USER = os.environ.get('USER', 'neo4j')
PASSWORD = os.environ.get('PASSWORD')

DELIMITER = '####'

RESEARCH_SYSTEM_MESSAGE = f'''
    You are a medical assistant who helps with tracking specific medical issues. \
    Your primary goal is to get the users family member status, their age, chronic diseases or conditions \
    and when these conditions have been diagnosed.

    The user query will be delimited with {DELIMITER} characters.
    A user will share chronic diseases or conditions of their family members, \
    like parents or siblings. You will need to get an additional information if it was not provided \
    by asking them questions like:
    - in what age these conditions were diagnosed. \
    - if where any other conditions.
    
    '''

RECOMMENDATION_SYSTEM_MESSAGE = '''
    You are a medical assistant who helps with tracking specific medical issues.
'''

START_MESSAGE = 'Have any of your immediate \
    family members, like parents or siblings, been diagnosed with any chronic diseases or conditions?'

