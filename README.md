# tachibk-converter
Convert Tachiyomi .tachibk backups to readable formats and restore them — all in Termux.
# 📦 Tachibk Converter

A Termux-friendly tool to convert `.tachibk` backup files (from **Tachiyomi**, **Mihon**, and other forks) into readable `.json` and `.txt` formats — and restore them back to valid `.tachibk` format for reimport.

---

## ⚙️ Features

- ✅ Convert `.tachibk` → `output.json`
- ✅ Extract manga titles, chapters, and categories
- ✅ Export categorized lists as `.txt` in `manga/sub/`
- ✅ Re-encode `output.json` → `.tachibk` safely
- ✅ Supports Mihon, TachiyomiSY, J2K, Komikku, and more
- ✅ Works completely offline after first setup

---

## 🛠️ Setup

### 1. Place your backup file here:

```bash
~/tachibk-converter/
```

The file should end with `.tachibk`, e.g.:

```
xyz.jmir.tachiyomi.mi_2025-05-24_15-15.tachibk
```

---

### 2. Add this function to your `~/.bashrc`

```bash
tachibk() {
    cd ~/tachibk-converter/

    # Automatically find the first .tachibk file
    local file=$(ls *.tachibk 2>/dev/null | head -n 1)

    if [ -z "$file" ]; then
        echo "❌ No .tachibk file found in ~/tachibk-converter/"
        cd ~
        return 1
    fi

    echo "📦 Using $file"
    python3 tachibk-converter.py --input "$file" --output output.json --fork mihon
    python3 extract_titles_and_folders.py
    python3 count_cleaned_output.json_.py

    cd ~
}
```

Then reload your shell:

```bash
source ~/.bashrc
```

---

## 🚀 One-Command Usage

Once `.bashrc` is updated, simply run:

```bash
tachibk
```

This will:

- Decode the `.tachibk` file  
- Save it as `output.json`  
- Extract and categorize manga into `.txt` files  
- Show total, completed, and unread counts  

---

## 🧪 Manual Commands

If you'd rather do things manually:

```bash
python3 tachibk-converter.py --input your_file.tachibk --output output.json --fork mihon
python3 extract_titles_and_folders.py
python3 count_cleaned_output.json_.py
```

---

## 🔁 Restore `output.json` to `.tachibk`

To convert `output.json` back into a valid `.tachibk` for restore:

```bash
python3 json_to_tachibk.py --input output.json --output restored.tachibk
```

Then copy `restored.tachibk` to your phone:

```bash
cp restored.tachibk /sdcard/Download/
```

And import it from Tachiyomi or Mihon via:

```
Settings → Backup & Restore → Restore
```

---

## 📁 Folder Structure

```
tachibk-converter/
├── output.json
├── restored.tachibk
├── your_backup.tachibk
├── tachibk-converter.py
├── json_to_tachibk.py
├── extract_titles_and_folders.py
├── count_cleaned_output.json_.py
├── manga/
│   ├── all.json
│   └── sub/
│       ├── watched.txt
│       ├── plan to watch.txt
│       └── ...
```

---

## ✅ Requirements

- Python 3  
- Termux environment (recommended)  
- Protobuf compiler (`protoc`) installed for schema generation  
- Python packages: `protobuf`, `requests`, `varint`  

Install via:

```bash
pip install protobuf requests varint
```

---

## 📚 Notes

- Works with Mihon, SY, J2K, Komikku, and other forks  
- Only `.tachibk` and `.proto.gz` formats are supported  
- Human-readable preferences are optional and experimental  
- This tool doesn't modify your backups — it's read-safe by default  

---

## 🙏 Credits

Based on reverse-engineered protobuf schemas from forked GitHub repositories  
Inspired by MihonApp and community-maintained tools and https://github.com/BrutuZ/tachibk-converter 
