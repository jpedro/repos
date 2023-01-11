import re

class Colors:
    RESET   = "\033[0m"
    RED     = "\033[31;1m"
    GREEN   = "\033[32;1m"
    YELLOW  = "\033[38;5;220m"
    BLUE    = "\033[34;1m"
    GRAY    = "\033[38;5;242m"
    PALE    = "\033[38;5;248m"
    PINK    = "\033[38;5;198;1m"
    PURPLE  = "\033[38;5;207m"
    ORANGE  = "\033[38;5;208m"


class Icons:
    DOT    = "•"
    FLAG   = "⚑"
    SQUARE = "▪"
    DIFF   = "±"
    UP     = "↑"
    DOWN   = "↓"
    SOLO   = "✖"

    GITHUB      = "" # ""
    BITBUCKET   = ""
    GITLAB      = ""
    HEROKU      = "\ue77b"
    AWS         = "\uf270"

    # SOLO   = "⏏"
    # SOLO   = "≡"
    # SOLO   = "⎈"
    # BOMB   = "💣"
    # DOT    = "."
    # DIFF   = "⬍"
    # UP     = "⇡"
    # DOWN   = "⇣"
    # UP     = "⬆"
    # DOWN   = "⬇"


# class Format:

#     COLORS = {
#         "bold": "1",
#         "green": "32;1",
#         "gray": "38;5;244",
#     }

#     # @staticmethod
#     # def color(match) -> str:
#     #     color = match.group(1)
#     #     text = match.group(2)
#     #     # print("-- COLOR", color)
#     #     # print("--  TEXT", text)
#     #     code = Format.COLORS.get(color)
#     #     if code:
#     #         return f"\033[{code}m{text}\033[0m"

#     #     return f"\033[{color}m{text}\033[0m"

#     @staticmethod
#     def text(text: str) -> str:
#         # Check for `*BOLD*`
#         text = re.sub("\*(.*?)\*", "\033[1m\\1\033[0m", text)
#         # Check for `_UNDERLINE_``
#         text = re.sub("\_(.*?)\_", "\033[4m\\1\033[0m", text)
#         # Parse for `c(<color> <text>)`
#         # text = re.sub("c\((.*?)\ (.*?)\)", "\033[\\1m\\2\033[0m", text)
#         text = re.sub("c\((.*?)\ (.*?)\)", Format.color, text)
#         text = re.sub("c\=(.*?)\ (.*)", Format.color, text)
#         # Parse for `b(<text>)`
#         # text = re.sub("b\((.*?)\)", "\033[1m\\1\033[0m", text)
#         return text
