import asyncio
import json
import aiohttp

HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'


async def generate_response(session: aiohttp.ClientSession, user_input, history):
    request = {
        'user_input': user_input,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'chat',
        'character': 'Ralsei-Serverbot',
        'your_name': 'User',
        'regenerate': False,
        '_continue': False,

        'preset': 'moddedDivineIntellect',
        'stopping_strings': ["\n[", "\n>", "]:", "\n#", "\n##", "\n###", "##", "###", "</s>", "000000000000", "1111111111", "0.0.0.0.", "1.1.1.1.", "2.2.2.2.", "3.3.3.3.", "4.4.4.4.", "5.5.5.5.", "6.6.6.6.", "7.7.7.7.", "8.8.8.8.", "9.9.9.9.", "22222222222222", "33333333333333", "4444444444444444", "5555555555555", "66666666666666", "77777777777777", "888888888888888", "999999999999999999", "01010101", "0123456789", "<noinput>", "<nooutput>"]
    }

    async with session.post(URI, json=request) as response:
        if response.status == 200:
            response_json = await response.json()
            result = response_json['results'][0]['history']
            chat_message = result['internal'][-1][1]
            print('\033[90m' + json.dumps(result, indent=4) + '\033[0m')
            print()
            print('\033[92m' + chat_message + '\033[0m')
            return result, chat_message


# async def test_data():
#     user_input = "[starsaligned]: hey ralsei, how do you feel right now"
#
#     history = {
#         "internal": [
#             [
#                 "<|BEGIN-VISIBLE-CHAT|>",
#                 "Greetings! I am Ralsei! You, it's wonderful to meet you!"
#             ]
#         ],
#         "visible": [
#             [
#                 "",
#                 "Greetings! I am Ralsei! You, it's wonderful to meet you!"
#             ]
#         ]
#     }
#
#     history_2msg = {
#         "internal": [
#             [
#                 "<|BEGIN-VISIBLE-CHAT|>",
#                 "Greetings! I am Ralsei! You, it's wonderful to meet you!"
#             ],
#             [
#                 "[pinheadtf2]: Hello, Ralsei! How are you doing?",
#                 "Hi there! I'm doing great, thank you very much! Just finished exploring another Dark World with my dear friends. Always keeps things interesting. How about you?"
#             ]
#         ],
#         "visible": [
#             [
#                 "",
#                 "Greetings! I am Ralsei! You, it's wonderful to meet you!"
#             ],
#             [
#                 "[pinheadtf2]: Hello, Ralsei! How are you doing?",
#                 "Hi there! I&#x27;m doing great, thank you very much! Just finished exploring another Dark World with my dear friends. Always keeps things interesting. How about you?"
#             ]
#         ]
#     }
#
#     async with aiohttp.ClientSession() as session:
#         await generate_response(session, user_input, history_2msg)
#
#
# asyncio.run(test_data())
