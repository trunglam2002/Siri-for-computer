import os


def write_to_notepad(text, directory):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Base filename and extension
    base_filename = "output"
    extension = ".txt"
    counter = 1

    # Determine the filename
    while True:
        filename = os.path.join(
            directory, f"{base_filename}{counter}{extension}")
        if not os.path.exists(filename):
            break
        counter += 1

    # Open the file in write mode and write the text
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    # Open the file with Notepad
    os.system(f"notepad.exe {filename}")


# Example usage
write_to_notepad("Hello, this is a test message written to Notepad!",
                 "C:/Users/NgLaam/Desktop/notepad.exe")
