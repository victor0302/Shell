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

        try:
            command = input().strip()
        except EOFError:
            break  
            
        if not command:
            continue 

        args = []
        current_token = ""
        in_single_quote = False

        for char in command:
            if char == "'":
                in_single_quote = not in_single_quote
            elif char == " ":
                if in_single_quote:
                    current_token += char
                else:
                    if len(current_token) > 0:
                        args.append(current_token)
                        current_token = ""
            else: 
                current_token += char

        if len(current_token) > 0:
            args.append(current_token)

        cmd_name = args[0]
        cmd_args = args[1:]

        if cmd_name == "exit":
            sys.exit(0)

        elif cmd_name == "pwd":
            print(os.getcwd())

        elif cmd_name == "cd":
            if len(cmd_args) > 0:
                path = cmd_args[0]
            else:
                path = "~"
        
            if path == "~":
                path = os.environ.get("HOME")
            
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")

        elif cmd_name == "type":
            if len(cmd_args) > 0:
                target = cmd_args[0]
                if target in builtin:
                    print(f"{target} is a shell builtin")
                else:
                    path = get_path(target)
                    if path:
                        print(f"{target} is {path}")
                    else:
                        print(f"{target}: not found")

        elif cmd_name == "echo":
            print(" ".join(cmd_args))

        else:
            path = get_path(cmd_name)
            
            if path:
                subprocess.run(args, executable=path)
            else:
                sys.stdout.write(f"{cmd_name}: command not found\n")

if __name__ == "__main__":
    main()