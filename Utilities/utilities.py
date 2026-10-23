import os


start="\033[91m"
end="\033[0m"

def log(text):
    if os.getenv("DEBUG")=="True":
        print(f"  {start}{text}{end}")