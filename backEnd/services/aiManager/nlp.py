import csv
import re

def nlp_clean_csv(csv_input_path, csv_output_path):
    stopwords = {"the", "and", "or"}

    cleaned_rows = []
    with open(csv_input_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        for row in reader:
            text = row["content"] if row["content"] else ""
            words = re.findall(r"\w+", text)
            filtered_words = [word for word in words if word.lower() not in stopwords]
            cleaned_text = " ".join(filtered_words)

            row["content"] = cleaned_text
            cleaned_rows.append(row)

    with open(csv_output_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Cleaned CSV created at {csv_output_path}")