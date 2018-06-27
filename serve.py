from dirtcastle.newapi import run_server


if __name__ == '__main__':
    run_server('0.0.0.0', 8000, use_debugger=True, use_reloader=True)
