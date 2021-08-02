from constants import HISTORY_FILE_PATH, HISTORY_LENGTH, PAGES_URL_ROOT


def format_history(history):
    return "\n".join(
        [f'<p><a href="{PAGES_URL_ROOT}/{name}">{name}</a></p>' for name in history]
    )


def read_history():
    try:
        with open(HISTORY_FILE_PATH) as historyfile:
            history = historyfile.read().split("\n")
        return history
    except IOError:
        return []


def write_history(history):
    with open(HISTORY_FILE_PATH, "w") as historyfile:
        historyfile.write("\n".join(history))


def update_history(new_name):
    history = read_history()
    history = [new_name] + [name for name in history if name != new_name]
    write_history(history[:HISTORY_LENGTH])
