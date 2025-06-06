# 📦 Tachibk Converter

A Termux-friendly tool to convert `.tachibk`, `.proto`, and `.proto.gz` backup files (from **Tachiyomi**, **Mihon**, and forks) into readable `.json` and `.txt` formats — and restore them back to valid `.tachibk` format.

---

## ⚙️ Features

- ✅ Convert `.tachibk`, `.proto`, or `.proto.gz` → `output/output.json`
- ✅ Interactive file selector based on saved backup time
- ✅ Export categorized manga to `.txt` in `manga/sub/`
- ✅ Export source-wise manga lists in `manga/extension/`
- ✅ Re-encode `output.json` → `.tachibk` safely
- ✅ Supports Mihon, TachiyomiSY, J2K, Komikku, and others
- ✅ Works entirely offline after setup

---

## 🛠️ Setup

### 1. Place your backup files in:

```bash
~/tachibk-converter/backup/
```

Supported formats:
- `.tachibk`
- `.proto`
- `.proto.gz`

Example:

```
backup/xyz.jmir.tachiyomi.mi_2025-06-06_11-09.tachibk
backup/tachiyomi_2023-10-02_00-51.proto.gz
```

---

### 2. Add this function to your `~/.bashrc`

```bash
tachibk() {
    cd ~/tachibk-converter/

    mkdir -p backup output

    echo "🔍 Scanning backup/ for backup files..."
    local files=($(ls -t backup/*.tachibk backup/*.proto backup/*.proto.gz 2>/dev/null))

    if [ ${#files[@]} -eq 0 ]; then
        echo "❌ No backup files found in backup/"
        cd ~
        return 1
    fi

    echo "📦 Found backup files:"
    local i=1
    for f in "${files[@]}"; do
        echo "  $i) $(basename "$f")"
        ((i++))
    done

    echo -n "➡️  Enter the number of the file to convert: "
    read -r selection

    if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt ${#files[@]} ]; then
        echo "❌ Invalid selection."
        cd ~
        return 1
    fi

    local file="${files[$((selection-1))]}"
    local filename=$(basename "$file")

    echo "📦 Selected: $filename"
    python3 tachibk-converter.py --input "$file" --output output/output.json --fork mihon

    if [ -f output/output.json ]; then
        echo "📂 Processing output/output.json..."
        python3 extract_titles_and_folders.py
        python3 count_cleaned_output.json_.py
    else
        echo "❌ Failed to create output/output.json"
    fi

    cd ~
}
```

Then reload your shell:

```bash
source ~/.bashrc
```

---

## 🚀 One-Command Usage

```bash
tachibk
```

This will:
- Let you pick a `.tachibk`, `.proto`, or `.proto.gz` file from `backup/`
- Convert it to `output/output.json`
- Extract and group manga into `manga/sub/` and `manga/extension/`
- Show read stats

---

## 🧪 Manual Usage

```bash
python3 tachibk-converter.py --input backup/your_file.tachibk --output output/output.json --fork mihon
python3 extract_titles_and_folders.py
python3 count_cleaned_output.json_.py
```

---

## 🔁 Restore JSON → `.tachibk`

```bash
python3 json_to_tachibk.py --input output/output.json --output restored.tachibk
cp restored.tachibk /sdcard/Download/
```

Then restore it in Tachiyomi or Mihon:

```
Settings → Backup & Restore → Restore
```

---

## 📁 Folder Structure

```
tachibk-converter/
├── backup/
│   └── *.tachibk / *.proto / *.proto.gz
├── output/
│   └── output.json
├── restored.tachibk
├── tachibk-converter.py
├── json_to_tachibk.py
├── extract_titles_and_folders.py
├── count_cleaned_output.json_.py
├── manga/
│   ├── all.json
│   ├── sub/
│   │   └── [category].txt
│   └── extension/
│       └── [source].txt
```

---

## ✅ Requirements

- Python 3  
- Termux or any Linux shell  
- Protobuf compiler (`protoc`) if generating schema  
- Python packages:

```bash
pip install protobuf requests varint
```

---

## 📚 Notes

- Works with Mihon, SY, J2K, Komikku, etc.
- Only `.tachibk`, `.proto`, `.proto.gz` are supported
- Preferences decoding is experimental
- Safe: does not modify original backups

---

## 🙏 Credits

- Based on [BrutuZ/tachibk-converter](https://github.com/BrutuZ/tachibk-converter)
- Extended and maintained by @Mohin2295747 for Termux + Mihon support