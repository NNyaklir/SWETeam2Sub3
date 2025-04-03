import random
import csv

class MarkovModel:
    def __init__(self):
        self.model = {}

    def train(self, data):
        for word in data:
            for i in range(len(word)):
                key = word[:i]
                next_char = word[i:i+1]
                if key not in self.model:
                    self.model[key] = []
                self.model[key].append(next_char)

    def generate(self, max_length=10):
        key = ""
        result = ""
        for _ in range(max_length):
            next_chars = self.model.get(key)
            if not next_chars:
                break
            next_char = random.choice(next_chars)
            result += next_char
            key = result[-len(key)-1:]
        return result

def generate_credentials(cleaned_csv_path, output_file='backend/data/crackedpass.txt'):
    # Load cleaned words
    words = []
    with open(cleaned_csv_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            content_words = row["content"].split()
            words.extend(content_words)

    # Train model and generate credentials
    model = MarkovModel()
    model.train(words)

    generated = [model.generate() for _ in range(10)]
    print("Generated credentials:", generated)

    with open(output_file, "w") as f:
        for cred in generated:
            f.write(cred + "\n")

    return generated