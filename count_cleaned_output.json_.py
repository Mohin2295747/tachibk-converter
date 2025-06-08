from collections import defaultdict
import json
import os

# === Load emoji.txt ===
def load_emoji_map(path="manga/emoji.txt"):
    emoji_map = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, emoji = line.strip().split(":", 1)
                    emoji_map[key.strip()] = emoji.strip()
    else:
        print("⚠️ emoji.txt not found. Emojis will be skipped.")
    return emoji_map

emoji_map = load_emoji_map()

# === Load all.json ===
with open("manga/all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Reading stats ===
total = len(data)
fully_read = sum(1 for m in data if m["read_chapters"] == m["total_chapters"] and m["total_chapters"] > 0)
unread = sum(1 for m in data if m["read_chapters"] == 0)
partial = total - fully_read - unread

print(f"📚 Total manga: {total}")
print(f"✅ Fully read: {fully_read}")
print(f"📖 Partially read: {partial}")
print(f"❌ Unread: {unread}")

# === Extension stats ===
extension_count = defaultdict(int)
for m in data:
    ext = m.get("extension", "Unknown")
    extension_count[ext] += 1

major_extensions = {}
minor_extensions = {}
for ext, count in extension_count.items():
    if count >= 10:
        major_extensions[ext] = count
    else:
        minor_extensions[ext] = count

print("\n📦 Manga per extension (sorted A–Z):")
for ext in sorted(major_extensions):
    emoji = emoji_map.get(ext, "•")
    print(f"{emoji} {ext}: {major_extensions[ext]}")

if minor_extensions:
    minor_names = ", ".join(sorted(minor_extensions.keys()))
    minor_total = sum(minor_extensions.values())
    print(f"• Other ({minor_names}): {minor_total}")

# === Category stats ===
category_count = defaultdict(int)
for m in data:
    categories = m.get("categories", ["Uncategorized"])
    for cat in categories:
        category_count[cat] += 1

print("\n🗂️ Manga per category (sorted A–Z):")
for cat in sorted(category_count):
    emoji = emoji_map.get(cat, "•")
    print(f"{emoji} {cat}: {category_count[cat]}")