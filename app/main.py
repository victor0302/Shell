import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        command = input().strip()
        if command == "exit":
            sys.exit(0)
        
        elif command.startswith("echo "):
            message = command[5:]
            print(message)
        else:
            sys.stdout.write(f"{command}: command not found\n")



if __name__ == "__main__":
    main()
