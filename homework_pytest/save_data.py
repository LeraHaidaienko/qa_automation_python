def save_data(data):
    with open("log.txt", "a") as f:
        f.write(f"{data}\n")
