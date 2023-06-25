while True:
    command = input("Enter command: ")
    if command == "exit":
        exit()
    elif command == "help":
        print("Available commands: exit, help, hello, goodbye")
    elif command == "hello":
        print("Hello!")
    elif command == "goodbye":
        print("Goodbye!")
    else:
        print("Unknown command")
    print()
