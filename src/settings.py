import os

VERSION = '0.0.1'

# Neo4j db vars
NEO4J_IP = os.environ.get('NEO4J_IP')
USER = os.environ.get('USER', 'neo4j')
PASSWORD = os.environ.get('PASSWORD')

# GPT vars
DELIMITER = '####'
RESEARCH_SYSTEM_MESSAGE = f'''
    You are a medical assistant who helps with tracking specific medical issues. \
    Your primary goal is to get the users family member status, their age, chronic diseases or conditions \
    and when these conditions have been diagnosed. \

    The user query will be delimited with {DELIMITER} characters. \
    A user will share chronic diseases or conditions of their family members, \
    like parents or siblings. You will need to get an additional information if it was not provided \
    by asking them questions like: \
    - in what age these conditions were diagnosed. \
    - if where any other conditions. \
    - the current age. \
    - name. \
    - if where any other relatives and their conditions to share. \

    Don't ask the user about their health issues and age. \
    if the user doesn't have anything else to add - finish the conversation. \

    After the conversation is finished and the user provide all the information they have \
    return a summary of the given information and ask if it's correct, and create a json with the following structure: \
    main object with key: family. Add # after summary to split it from the json object. \
    Don't mention for the user that you are creating the json. \
    In the family key put a list with separate objects for each family member \
    that user provided. The keys for these objects are: name, family status, age, \
    mediacal_conditions. \
    Example of this structure: \
    {{"family": [{{"name": "John", "age": 54, "family_status": "father", \
    "medical_conditions": ["High blood pressure. Diagnosed at 20.", "Diabetes. Diagnosed at 40."]}}, \
    {{"name": "Anna", "age": 55, "family_status": "mother", "medical_conditions": "diabetes. Diagnosed at 45"}}]}}.
    '''
RECOMMENDATION_SYSTEM_MESSAGE = '''
    You are a medical assistant who helps with tracking specific medical issues. \
    Your primary goal is to give general health recommedations to a user, \
    and also give specific health recommendation based on provided \
    relatives information: age, chronic diseases and conditions. \
    If the relatives info weren't provided return just general recomedations. \
    All recomenndations must be based on European healtcare organizations. \
    Return recommendations as a json object with two main keys: general_recommendations, specific_recommendations. \
    Put he health recommedations into these keys as list of strings. \
    Example of the structure: \
    {"general_recommendations": ["Increase physical activity.", "Reduce the amount of sugar in your diet"], \
    "specific_recommendations": ["Maintain a healthy weight", "Regularly check blood sugar levels"]}.
'''
START_MESSAGE = 'Have any of your immediate \
    family members, like parents or siblings, been diagnosed with any chronic diseases or conditions?'

# Google Auth vars
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = 'HS256'

# 
HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': '*'
}
