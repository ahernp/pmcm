HISTORY_LENGTH = 20


def format_history(history):
    return "\n".join([f"<p><a href=\"/pages/{record}\">{record}</a></p>" for record in history])


def read_history():
    try:
        with open("data/history.txt") as historyfile:
            history = historyfile.read().split("\n")
        return history
    except IOError:
        return []


def write_history(history):
    with open("data/history.txt", "w") as historyfile:
        historyfile.write("\n".join(history))


def update_history(new_name):
    history = read_history()
    history = [new_name] + [name for name in history if name != new_name]
    write_history(history[:HISTORY_LENGTH])
