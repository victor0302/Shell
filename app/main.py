import sys
import os
import subprocess

def get_path(cmd):
    env_path = os.environ.get("PATH", "")
    
    paths = env_path.split(os.pathsep)
    
    for path in paths:
        full_path = os.path.join(path, cmd)
        
        if os.access(full_path, os.X_OK):
            return full_path
            
    return None

def main():
    builtin = {"echo", "exit", "type", "pwd", "cd"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        command = input().strip()
        if command == "exit":
            sys.exit(0)

        elif command == "pwd":
            print(os.getcwd())

        elif command.startswith("cd "):
            path = command[3:].strip()
        
            if path == "~":
                path = os.environ.get("HOME")
            
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")

        elif command.startswith("type"):
            message = command[5:]
            if message in builtin:
                print(f"{message} is a shell builtin")
            else:
                path = get_path(message)
                if path:
                    print(f"{message} is {path}")
                else:
                    print(f"{message}: not found")

        elif command.startswith("echo "):
            message = command[5:]
            print(message)

        else:
            args = command.split()
            program_name = args[0]
            
            path = get_path(program_name)
            
            if path:
                subprocess.run(args, executable=path)
            else:
                sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
