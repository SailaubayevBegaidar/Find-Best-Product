import random
import string
import json

def generate_random_url(base_url, start_id, end_id, num_urls):
    urls = []

    for _ in range(num_urls):
        random_id = random.randint(start_id, end_id)
        random_suffix = ''.join(random.choices(string.ascii_letters, k=5))
        url = f"{base_url}{random_id}/{random_suffix}"
        urls.append(url)

    return urls

if __name__ == "__main__":
    base_url = "https://www.microcenter.com/product/"
    start_id = 505000
    end_id = 675500
    num_urls = 30

    random_urls = generate_random_url(base_url, start_id, end_id, num_urls)

    output_file = "generated_urls.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump({"urls": random_urls}, file, ensure_ascii=False, indent=4)

    print(f"Generated URLs saved to {output_file}.")
