"""
A simplified implementation of ELIZA
"""
__author__ = "Pierre Nugues"

import regex as re
import numpy as np

dialogue_pairs = {
    '.*I am not (.+)': [
        r'Why aren\'t you \1'
    ],
    '.*I am (.+)': [
        r'How long have you been \1'
    ],
    '.*I like (.+)': [
        r'Why do you like \1'
    ],
    '.*I remember (.+)': [
        r'Do you often think of \1',
        'What else do you remember',
        r'Why do you remember \1 just now'
    ],
    '.*(father|mother|brother|sister).*': [
        r'Please tell me more about your \1'
    ],
    '^no$': [
        'Why are you so negative?',
        'Why not?'
    ],
    '^\p{L}+$': [
        'Tell me more...'
    ],
    # When nothing matches
    '.*': [
        'I am not sure I understand you fully',
        'Please go on',
        'What does that suggest to you'
    ]
}


def match_utterance(user_input):
    """
    match_utterance accepts the user's utterance and
    tries to find a template matching it
    """
    for key in dialogue_pairs:
        matches = list(re.finditer(key, user_input))
        if matches:
            choice = np.random.randint(len(dialogue_pairs[key]))
            answer = re.sub(key, dialogue_pairs[key][choice],
                            user_input, count=1)
            return answer


# The main loop reads the input and calls match_utterance
# It stops when the input is the word bye.
print('Hello, I am ELIZA. How can I help you?')
user_input = input('User: ')
while user_input.lower() != 'bye':
    answer = match_utterance(user_input)
    print('Eliza:', answer)
    user_input = input('User: ')
print('Eliza:', 'Bye')
