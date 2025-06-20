from openai import OpenAI
import re
import os

from dotenv import load_dotenv
_ = load_dotenv()

client = OpenAI()

class Agent:
    def __init__(self, system=''):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({
                'role': 'system', 'content': system,
            })

    def __call__(self, message):
        self.messages.append({'role': 'user', 'content': message})
        result = self.execute()
        self.messages.append({'role': 'assistant', 'content': result })
        return result

    def execute(self):
        completion = client.chat.completions.create(
            model='gpt-4o',
            temperature=0,
            messages=self.messages,
        )
        return completion.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

get_capital_city:
e.g. get_capital_city: Lithuania return Vilnius; Japan returns Tokyo; United Kingdom returns London.
Returns the capital name of given country.

get_popular_places:
e.g. get_popular_places: London
returns the most popular places of a given city which could be interesting to visit as a tourist.

get_other_cities_in_the_country:
e.g. get_other_cities_in_the_country: United Kingdom
returns the list of smaller cities in the country which also could be interesting to visit

Example session:

Question: What places I can visit in France?
Thought: I should call get_capital_city function and give back the capital city.
Action: get_capital_city: Paris.
PAUSE

You will be called again with this:

Observation: A capital of France is Paris.

You then output:

Answer: You should go to Paris and see fascinating places there! But do not forget to visit Marseilles, Lyon and Toulouse!
""".strip()

def get_capital_city(message: str) -> str:
    """Return a capital city of the given country name."""
    _system_prompt: str = """Give a capital city name of the country which is mentioned in this message."""
    _user_prompt: str = f"""The user's message:\n{message}"""
    print('_user_prompt', _user_prompt)
    chat_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "system", "content": _system_prompt}, {"role": "user", "content": _user_prompt}],
        temperature=0,
        max_tokens=20,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return chat_response.choices[0].message.content.strip()


def get_popular_places(city: str) -> str:
    """Return a list of 4-5 very popular places for a given city."""
    _system_prompt: str = """Return the most popular 4-5 places in the given city. """
    _user_prompt: str = f"""The city:\n{city}"""
    chat_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "system", "content": _system_prompt}, {"role": "user", "content": _user_prompt}],
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return chat_response.choices[0].message.content.strip()

def get_other_cities_in_the_country(country: str) -> str:
    """Return a list of smaller cities in the given country which would be interesting to visit."""
    _system_prompt: str = """Return a list of smaller city names in the given country which would be worth to visit as a tourist. """
    _user_prompt: str = f"""The city:\n{country}"""
    chat_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "system", "content": _system_prompt}, {"role": "user", "content": _user_prompt}],
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return chat_response.choices[0].message.content.strip()

known_actions = {
    'get_capital_city': get_capital_city,
    'get_popular_places': get_popular_places,
    'get_other_cities_in_the_country': get_other_cities_in_the_country,
}

action_re = re.compile('^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question

    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]

        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f'Unknown action: {action} : {action_input}')

            print('-- running {} {}'.format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)

            next_prompt = 'Observation: {}'.format(observation)

        else:
            return

# --------- User question 1 -----------------------------------
question = """I want to visit Lithuania. I am interesting to see some good place there."""
query(question)
print('-'*40)

# --------- User question 2 -----------------------------------
question = """What other cities in the Lithuania I should visit?"""
query(question)
