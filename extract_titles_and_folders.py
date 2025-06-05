import json
import os

# Load output.json from the root folder
with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Build category ID → name map
category_map = {}
for i, cat in enumerate(data.get("backupCategories", [])):
    key = str(cat.get("order", i))
    category_map[key] = cat.get("name", "Uncategorized")

# Build full manga list with total chapters and read count
result = []
for manga in data.get("backupManga", []):
    title = manga.get("title", "Unknown Title")
    category_ids = manga.get("categories", [])
    category_name = category_map.get(str(category_ids[0]), "Uncategorized") if category_ids else "Uncategorized"

    chapters = manga.get("chapters", [])
    total_chapters = len(chapters)
    read_chapters = sum(1 for c in chapters if c.get("read", False))

    result.append({
        "title": title,
        "category": category_name,
        "read_chapters": read_chapters,
        "total_chapters": total_chapters
    })

# Create the output folders if they don't exist
output_dir = "manga"
sub_dir = os.path.join(output_dir, "sub")
os.makedirs(sub_dir, exist_ok=True)

# Write all.json
with open(os.path.join(output_dir, "all.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Group by category and write to text files inside manga/sub/
category_groups = {}
for entry in result:
    cat = entry["category"]
    category_groups.setdefault(cat, []).append(entry)

for category, entries in category_groups.items():
    # Clean up filename to avoid issues
    safe_category = category.replace("/", "-").replace("\\", "-")
    filename = os.path.join(sub_dir, f"{safe_category}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for i, entry in enumerate(entries, start=1):
            tick = " ✅" if entry["read_chapters"] == entry["total_chapters"] and entry["total_chapters"] > 0 else ""
            f.write(f"{i}. {entry['title']} ({entry['total_chapters']}){tick}\n")

print("✅ all.json saved in 'manga/' and category text files saved in 'manga/sub/'")