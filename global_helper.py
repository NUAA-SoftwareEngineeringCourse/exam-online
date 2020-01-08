import os


def cmd_exec(cmd: str):
    print('[exec cmd]', cmd)
    if os.system(cmd) != 0:
        print('[exec cmd]', cmd, 'failed')
        return False
    return True


