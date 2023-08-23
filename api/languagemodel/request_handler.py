import asyncio
import json
import aiohttp

HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'


async def generate_response(user_input, history):
    request = {
        'user_input': user_input,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'chat',
        'character': 'Ralsei',
        'instruction_template': 'Airoboros-v1.2',  # Will get autodetected if unset
        'your_name': 'User',
        'regenerate': False,
        '_continue': False,
        'chat_instruct_command': 'Continue the chat dialogue below. '
                                 'Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        'preset': 'moddedDivineIntellect',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URI, json=request) as response:
            if response.status == 200:
                response_json = await response.json()
                result = response_json['results'][0]['history']
                print(json.dumps(result, indent=4))
                # print()
                # print(result['visible'][-1][1])


async def test_data():
    user_input = "Hello, Ralsei! How are you doing?"

    history = {
        "internal": [
            [
                "<|BEGIN-VISIBLE-CHAT|>",
                "Greetings! I am Ralsei! You, it's wonderful to meet you!"
            ]
        ],
        "visible": [
            [
                "",
                "Greetings! I am Ralsei! You, it's wonderful to meet you!"
            ]
        ]
    }

    await generate_response(user_input, history)


asyncio.run(test_data())
