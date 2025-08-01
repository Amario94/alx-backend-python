def get_thread(message):
    thread = []
    def fetch_replies(msg):
        for reply in msg.replies.all():
            thread.append(reply)
            fetch_replies(reply)
    fetch_replies(message)
    return thread
