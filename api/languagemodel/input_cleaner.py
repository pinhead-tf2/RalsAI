import re
from difflib import ndiff


# list for banned words, automatically catching similar mis-spellings or bypasses
# only really works for words at or above 5 letters
banned_words_list = ['pornography', 'hentai', 'penis']

# banned works, only works on exact matches
banned_words_exact_regex = "\b(naked|cock|penis|balls|boobs|explicit|nsfw|p0rn|pron|pr0n|butt|booty|s3x|n4ked|r34)\b"


async def detect_banned_words(unscreened_input: str):
    detected_words = []
    unscreened_words_list = unscreened_input.split()

    for word in unscreened_words_list:
        alphanumeric_word = re.sub("[^a-zA-Z0-9]+", "", word)
        threshold = 0
        word_length = len(alphanumeric_word)

        if word_length > 2:
            if word_length > 6:
                threshold = 2
            elif word_length > 4:
                threshold = 1

            for banned_word in banned_words_list:
                if await get_levenshtein_distance(alphanumeric_word, banned_word) <= threshold:
                    print('\033[93m' + f'Banned word detected: {word} similar to {banned_word}' + '\033[0m')
                    detected_words.append(word)

    if len(detected_words) > 0:
        print('All detected words: ' + str(detected_words) + '\n')

    return detected_words


# https://codereview.stackexchange.com/a/217074
# big thanks to this guy
async def get_levenshtein_distance(str1, str2, ):
    counter = {"+": 0, "-": 0}
    distance = 0
    for edit_code, *_ in ndiff(str1, str2):
        if edit_code == " ":
            distance += max(counter.values())
            counter = {"+": 0, "-": 0}
        else:
            counter[edit_code] += 1
    distance += max(counter.values())
    return distance
