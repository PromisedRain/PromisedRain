from datetime import date
import json
import re

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

index = date.today().toordinal() % len(quotes)
selected = quotes[index]

quote_text = selected.get("quote", "...")
author_text = selected.get("author")

quote_block = f"> *{quote_text}*"
if author_text:
    quote_block += f"\n> — *{author_text}*"

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"(<!--QUOTE_START-->)(.*?)(<!--QUOTE_END-->)"
new_content = re.sub(
    pattern,
    f"\\1\n{quote_block}\n\\3",
    content,
    flags=re.DOTALL
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)
