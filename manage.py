import os
import sys

import importlib


def run_script(command):
    try:
        script_name = ""
        if command == "train":
            script_name = "train_entrance"
            # subprocess.run(["python", "train_entrance.py"], check=True)
        elif command == "predict":
            script_name = "server"
            # subprocess.run(["python", "server.py"], check=True)
        elif command == "test":
            script_name = "test"
        if script_name != "":
            print(f"run command {command}")
            module = importlib.import_module(script_name)
            module.main()
        else:
            print("do nothing")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        run_script(command)
    else:
        command = os.environ.get('CMD', '')
        run_script(command)
