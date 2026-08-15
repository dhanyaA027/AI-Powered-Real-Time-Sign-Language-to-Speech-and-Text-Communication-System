from collections import Counter, deque

class SignLogic:
    # Temporal smoothing + confidence filtering + duplicate suppression.
    def __init__(self, window=8, min_votes=5):
        self.window = deque(maxlen=window)
        self.min_votes = min_votes
        self.last_committed = None
        self.sentence = []

    def update(self, label, confidence=1.0):
        if not label or confidence <= 0:
            return None
        self.window.append(label)
        current, votes = Counter(self.window).most_common(1)[0]
        if votes >= self.min_votes and current != self.last_committed:
            self.last_committed = current
            return current
        return None

    def commit(self, label):
        if label:
            self.sentence.append(label.replace("_", " "))

    def clear(self):
        self.window.clear()
        self.last_committed = None
        self.sentence.clear()

    def text(self):
        return " ".join(self.sentence)
