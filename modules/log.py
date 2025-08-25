
def log(content):
    from datetime import datetime
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {content}\n")
