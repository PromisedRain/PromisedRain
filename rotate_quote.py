import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path


quotes_path = Path("quotes.json")
cache_path = Path(".quote_cache.json")
readme_path = Path("README.md")


with quotes_path.open("r", encoding="utf-8") as f:
    quotes = json.load(f)

if not quotes:
    raise ValueError("quotes.json is empty!")

# get previous quote idx
last_index = None
if cache_path.exists():
    try:
        with cache_path.open("r", encoding="utf-8") as f:
            cache = json.load(f)
        last_index = cache.get("last_index")
    except (json.JSONDecodeError, TypeError):
        last_index = None

indices = list(range(len(quotes)))
if last_index is not None and len(quotes) > 1:
    indices.remove(last_index)

selected_index = random.choice(indices)
selected = quotes[selected_index]

with cache_path.open("w", encoding="utf-8") as f:
    json.dump({"last_index": selected_index}, f)

quote_text = selected.get("quote", "...").strip()
author_text = selected.get("author", "").strip()

#if author_text:
#    quote_block = f"> *{quote_text}*  \n> — **{author_text}**"
#else:
#    quote_block = f"> *{quote_text}*"

if quote_text and quote_text[-1] not in ".!?…":
    quote_text += "."
if author_text and author_text[-1] not in ".!?…":
    author_text += "."


paragraphs = quote_text.split("\n\n")
quote_lines = []

for para in paragraphs:
    lines = para.split("\n")
    for line in lines:
        if line.strip():
            quote_lines.append(f"> *{line.strip()}*  ")
    quote_lines.append(">")

if author_text:
    quote_lines.append(">")
    quote_lines.append(f"> — **{author_text}**")

quote_block = "\n".join(quote_lines)

with readme_path.open("r", encoding="utf-8") as f:
    content = f.read()

pattern = r"(<!--QUOTE_START-->)(.*?)(<!--QUOTE_END-->)"
new_content = re.sub(pattern, f"\\1\n{quote_block}\n\\3", content, flags=re.DOTALL)

timestamp = f"<!-- last updated: {datetime.now(timezone.utc).isoformat()} -->"
if "<!-- last updated:" in new_content:
    new_content = re.sub(r"(<!-- last updated:).*?-->", timestamp, new_content)
else:
    new_content = re.sub(r"(<!--QUOTE_END-->)", f"\\1\n{timestamp}", new_content)

with readme_path.open("w", encoding="utf-8") as f:
    f.write(new_content)

print("README updated with a new quote and timestamp.")
