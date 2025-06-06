import json
import os

# Load output.json from the root folder
with open("output/output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Build category ID → name map
category_map = {}
for i, cat in enumerate(data.get("backupCategories", [])):
    key = str(cat.get("order", i))
    category_map[key] = cat.get("name", "Uncategorized")

# Build sourceId → extension name map
source_map = {}
for src in data.get("backupSources", []):
    source_map[str(src.get("sourceId"))] = src.get("name", "Unknown")

# Build full manga list with total chapters, read count, and extension
result = []
for manga in data.get("backupManga", []):
    title = manga.get("title", "Unknown Title")
    category_ids = manga.get("categories", [])
    category_name = category_map.get(str(category_ids[0]), "Uncategorized") if category_ids else "Uncategorized"
    source_id = str(manga.get("source", ""))
    extension = source_map.get(source_id, f"Unknown ({source_id})")

    chapters = manga.get("chapters", [])
    total_chapters = len(chapters)
    read_chapters = sum(1 for c in chapters if c.get("read", False))

    result.append({
        "title": title,
        "category": category_name,
        "extension": extension,
        "read_chapters": read_chapters,
        "total_chapters": total_chapters
    })

# Create output folders
output_dir = "manga"
sub_dir = os.path.join(output_dir, "sub")
ext_dir = os.path.join(output_dir, "extension")
os.makedirs(sub_dir, exist_ok=True)
os.makedirs(ext_dir, exist_ok=True)

# Clean sub_dir and ext_dir
for folder in [sub_dir, ext_dir]:
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

# Write all.json with extensions included
with open(os.path.join(output_dir, "all.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Group by category and write to manga/sub/*.txt
category_groups = {}
for entry in result:
    cat = entry["category"]
    category_groups.setdefault(cat, []).append(entry)

for category, entries in category_groups.items():
    safe_category = category.replace("/", "-").replace("\\", "-")
    filename = os.path.join(sub_dir, f"{safe_category}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for i, entry in enumerate(entries, start=1):
            tick = " ✅" if entry["read_chapters"] == entry["total_chapters"] and entry["total_chapters"] > 0 else ""
            f.write(f"{i}. {entry['title']} ({entry['total_chapters']}) [{entry['extension']}] {tick}\n")

# Group by extension and write to manga/extension/*.txt
extension_groups = {}
for entry in result:
    ext = entry["extension"]
    extension_groups.setdefault(ext, []).append(entry)

for extension, entries in extension_groups.items():
    safe_extension = extension.replace("/", "-").replace("\\", "-")
    filename = os.path.join(ext_dir, f"{safe_extension}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for i, entry in enumerate(entries, start=1):
            tick = " ✅" if entry["read_chapters"] == entry["total_chapters"] and entry["total_chapters"] > 0 else ""
            f.write(f"{i}. {entry['title']} ({entry['total_chapters']}) [{entry['category']}] {tick}\n")

print("✅ all.json updated with extensions.")
print("📁 category text files saved in 'manga/sub/'")
print("📁 extension text files saved in 'manga/extension/'")
