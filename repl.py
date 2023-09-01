import morsecode
from morsecode import lexer, translator

REPL_CMD_DOCS = {
    "HELP": "Show REPL command help.",
    "TO": "Convert subsequent text to Morse Code.",
    "FROM": "Convert subsequent text from Morse Code.",
    "STRICT_TO": "Convert subsequent text to Morse Code.",
    "STRICT_FROM": "Convert subsequent text from Morse Code.",
    "QUIT": "Exit REPL.",
}


def welcome() -> None:
    print("*** Welcome to the Morse Code REPL! ***")
    help()


def help(text_in=None) -> bool:
    print("Enter a REPL command.  Supported commands include:")
    for doc in REPL_CMD_DOCS:
        print("\t{}\t{}".format(doc, REPL_CMD_DOCS[doc]))
    return True


def quit(text_in) -> bool:
    print("Exiting REPL now.")
    return False


def invalid_cmd(text_in) -> bool:
    print("Invalid command: " + text_in)
    return True


def convert_to(text_in) -> bool:
    print(
        translator.Translator(lexer.Lexer(text_in, True, False).tokenize()).translate()
    )
    return True


def convert_from(text_in) -> bool:
    print(
        translator.Translator(
            lexer.Lexer(text_in, False, False).tokenize(), False
        ).translate()
    )
    return True


def convert_to_strict(text_in) -> bool:
    try:
        print(translator.Translator(lexer.Lexer(text_in).tokenize()).translate())
    except lexer.UnhandledCharacterException as ex:
        print(ex)
    return True


def convert_from_strict(text_in) -> bool:
    try:
        print(
            translator.Translator(
                lexer.Lexer(text_in, False).tokenize(), False
            ).translate()
        )
    except lexer.UnhandledCharacterException as ex:
        print(ex)
    return True


REPL_CMDS = {
    "HELP": [help],
    "TO": [convert_to],
    "FROM": [convert_from],
    "STRICT_TO": [convert_to_strict],
    "STRICT_FROM": [convert_from_strict],
    "QUIT": [quit],
}


def main() -> None:
    repl = True
    while repl:
        text_in = input("mc >> ")
        cmd_index = text_in.find(" ")
        if cmd_index < 0:
            cmd = text_in.upper()
            arg = ""
        else:
            cmd = text_in[:cmd_index].upper()
            arg = text_in[cmd_index + 1 :]

        if cmd in REPL_CMDS:
            action = REPL_CMDS[cmd]
            repl = action[0](arg)
        else:
            invalid_cmd(text_in)


if __name__ == "__main__":
    """REPL (Read, Evaluate, Print, Loop)"""
    welcome()
    main()
