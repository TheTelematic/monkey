import os

if os.getenv("DEBUG"):
    import subprocess

    subprocess.run(["pip", "install", os.getenv("DEBUG_PYDEVD_PYCHARM")])
    import pydevd_pycharm

    pydevd_pycharm.settrace(
        os.getenv("DEBUG_HOST"),
        port=int(os.getenv("DEBUG_PORT")),
        stdoutToServer=True,
        stderrToServer=True,
        suspend=False,
    )
