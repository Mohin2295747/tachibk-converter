import json
from collections import defaultdict

# Load all.json
with open("manga/all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Original Stats ===
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
    extension = m.get("extension", "Unknown")
    extension_count[extension] += 1

print("\n📦 Manga per extension:")
for ext, count in sorted(extension_count.items(), key=lambda x: -x[1]):
    print(f"• {ext}: {count}")