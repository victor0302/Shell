import sys
import os


def main():
    builtin = {"echo","exit","type"}
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        command = input().strip()
        if command == "exit":
            sys.exit(0)

        elif command.startswith("type"):
            message = command [5:]
            if message in builtin:
                print(f"{message} is a shell builtin")
            else:
                env_path = os.environ.get("PATH")
                paths = env_path.split(os.pathsep)
                found = False

                for path in paths:
                    full_address = os.path.join(path,message)
                    
                    if os.access(full_address, os.X_OK):
                        print(f"{message} is {full_address}")
                        found = True
                        break
                if not found:
                    print(f"{message}: not found")


        elif command.startswith("echo "):
            message = command[5:]
            print(message)

        else:
            sys.stdout.write(f"{command}: command not found\n")



if __name__ == "__main__":
    main()
