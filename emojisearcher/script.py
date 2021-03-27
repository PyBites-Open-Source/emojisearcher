import re

from emoji import EMOJI_UNICODE
from pyperclip import copy

QUIT = 'q'
SIGNAL_CHAR = '.'
PROMPT = f"""
------------------------------------------------------------------------------------
Type one or more emoji related words ...
End a word with a {SIGNAL_CHAR} if you want to select an emoji if there are multiple
matches, otherwise the first match will be picked. Type 'q' to exit.
> """
NON_EMOJI_CHARS = re.compile('[^\U00010000-\U0010ffff]',
                             flags=re.UNICODE)
LANGUAGE = 'en'  # emoji lib also supports es, pt and it
EMOJI_MAPPING = EMOJI_UNICODE[LANGUAGE]


def clean_non_emoji_characters(emoji: str) -> str:
    return NON_EMOJI_CHARS.sub(r'', emoji)


def get_matching_emojis(
    words: list[str], interactive: bool = False
) -> list[str]:
    """Traverse words list finding matching emojis.
       If there are multiple matches take the first one unless
       interactive is set to True or the word ends with a SIGNAL_CHAR,
       which means user specified desire for interactive lookup.
    """
    matches = []
    for word in words:
        emojis = get_emojis_for_word(word.rstrip(SIGNAL_CHAR))
        if len(emojis) == 0:
            continue

        interactive_mode = word.endswith(SIGNAL_CHAR) or interactive
        if len(emojis) > 1 and interactive_mode:
            selected_emoji = user_select_emoji(emojis)
        else:
            selected_emoji = emojis[0]

        matches.append(
            clean_non_emoji_characters(selected_emoji))

    return matches


def get_emojis_for_word(
    word: str, emoji_mapping: dict[str, str] = EMOJI_MAPPING
) -> list[str]:
    # TODO: mypy says "Incompatible types in assignment"
    return [emo for name, emo in emoji_mapping.items() if word in name]


def user_select_emoji(emojis: list[str]) -> str:
    while True:
        try:
            for i, emo in enumerate(emojis, start=1):
                print(i, emo)
            user_input = input("Select the number of the emoji you want: ")
            idx = int(user_input)
            return emojis[idx - 1]
        except ValueError:
            print(f"{user_input} is not an integer: ")
            continue


def copy_emojis_to_clipboard(matches: list[str]) -> None:
    all_matching_emojis = ' '.join(matches)
    print(f"Copying {all_matching_emojis} to clipboard")
    copy(all_matching_emojis)


def main():
    while True:
        user_input = input(PROMPT)
        user_input = user_input.lower()
        if user_input == QUIT:
            print('Bye')
            break

        words = user_input.split()
        matches = get_matching_emojis(words)
        if matches:
            copy_emojis_to_clipboard(matches)
        else:
            print(f"No matches for {user_input}")


if __name__ == "__main__":
    main()