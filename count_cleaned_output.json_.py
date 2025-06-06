import json
from collections import defaultdict

# Load all.json
with open("manga/all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Read Stats ===
total = len(data)
fully_read = sum(1 for m in data if m["read_chapters"] == m["total_chapters"] and m["total_chapters"] > 0)
unread = sum(1 for m in data if m["read_chapters"] == 0)
partial = total - fully_read - unread

print(f"📚 Total manga: {total}")
print(f"✅ Fully read: {fully_read}")
print(f"📖 Partially read: {partial}")
print(f"❌ Unread: {unread}")

# === Extension Stats ===
extension_count = defaultdict(int)

for m in data:
    ext = m.get("extension", "Unknown")
    extension_count[ext] += 1

# Split into major and minor extensions
major_extensions = {}
minor_extensions = {}

for ext, count in extension_count.items():
    if count >= 10:
        major_extensions[ext] = count
    else:
        minor_extensions[ext] = count

print("\n📦 Manga per extension (sorted A-Z):")

# Print major extensions alphabetically
for ext in sorted(major_extensions):
    print(f"• {ext}: {major_extensions[ext]}")

# Print combined minor extensions
if minor_extensions:
    minor_names = ", ".join(sorted(minor_extensions.keys()))
    minor_total = sum(minor_extensions.values())
    print(f"• Other ({minor_names}): {minor_total}")

# === Category Stats ===
category_count = defaultdict(int)

for m in data:
    cat = m.get("category", "Uncategorized")
    category_count[cat] += 1

print("\n🗂️ Manga per category (sorted A-Z):")
for cat in sorted(category_count):
    print(f"• {cat}: {category_count[cat]}")