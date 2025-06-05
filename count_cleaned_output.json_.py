import json

with open("manga/all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = len(data)
fully_read = sum(1 for m in data if m["read_chapters"] == m["total_chapters"] and m["total_chapters"] > 0)
unread = sum(1 for m in data if m["read_chapters"] == 0)
partial = total - fully_read - unread

print(f"📚 Total manga: {total}")
print(f"✅ Fully read: {fully_read}")
print(f"📖 Partially read: {partial}")
print(f"❌ Unread: {unread}")