# GAL (Get All URLs) - Burp Suite Extension

**GAL** is a powerful, flexible Burp Suite extension that helps you extract URLs based on file type or pattern matching from the Target > Site Map tab. It’s designed for speed, usability, and convenience — making repetitive tasks like pulling out `.js`, `.css`, `.png`, or API endpoints a breeze.

---

## 🚀 Features

### 🎯 Match by File Extension
Extract URLs ending in specific extensions (e.g., `js`, `css`, `png`).  
Only want `.js` files? You got it.

### 🧠 Full Regex Support
Prefer regex for advanced filtering? You can switch to full custom pattern mode (e.g., `.*api.*`, `.*\.(js|json)$`).

### 🔘 Mode Toggle (Extension OR Regex)
To avoid confusion, only one mode is active at a time — either extension-based or regex-based.

### 📁 Output Options
Choose between:
- A single output file for all matched URLs.
- Domain-based folders with separate files for each host.

### 🕒 Timestamped Output Files
All extracted files are automatically timestamped, preventing accidental overwrites and helping with version tracking.

### 📋 Optional Clipboard Copying
You can choose to automatically copy all extracted URLs to your clipboard right after export.

### 🖱️ Seamless UI Integration
Right-click in the **Target > Site Map**, select hosts or folders, and choose:  
`Extract URLs by file type or regex`

---

## 🛠 Requirements

- Burp Suite (Community or Professional)
- [Jython standalone JAR](https://www.jython.org/download) (e.g., `jython-standalone-2.7.3.jar`)

---

## 🧩 Installation

1. Open Burp Suite.
2. Go to **Extensions > Installed > Add**.
3. Select:
   - **Extension Type**: `Python`
   - **Extension File**: `GAL.py`
   - **Python Environment**: Browse to your Jython standalone JAR.
4. Click **Next** — done!

---

## 💾 Output Format

- Files are saved in a directory of your choice.
- Output filename format:

```
extracted_urls_YYYYMMDD_HHMMSS.txt
```

- If “Split by domain” is enabled:

```
/selected/path/
├── example.com/
│   └── extracted_urls_20250407_143210.txt
├── testsite.net/
│   └── extracted_urls_20250407_143210.txt
```

---

## 📌 Example Use Cases

- Quickly extract all JavaScript files from one or more targets.
- Identify API endpoints across selected domains with regex like `.*api.*`.
- Export sitemap-derived assets for use with tools like Intruder, custom scanners, or for manual analysis.
- Copy URLs directly to clipboard for fast pasting into terminals, notes, or tools.

---

## 👨‍💻 Author

Built with 🧠, ☕, and Burp by **gokuKaioKen**  
Feel free to fork, improve, or submit pull requests!

---

## 🧪 Usage

1. **Navigate to the Target tab in Burp Suite.**

2. Expand the **Site Map** and select one or more target domains or folders.

3. **Right-click** your selection and choose:

   ```
   Extract URLs by file type or regex
   ```

4. In the popup dialog:
   - Choose **Match by extension** or **Use full regex pattern**.
   - Enter your extensions (e.g. `js,css`) or a regex (e.g. `.*api.*`).
   - Optionally check:
     - ✅ Split output into separate domain folders
     - ✅ Copy results to clipboard

5. Click **OK**.

6. You'll be prompted to **select a directory** where results will be saved.

7. A confirmation will appear showing how many URLs were extracted and saved.
   - If clipboard option was checked, the results are ready to paste!

---

📝 Output files will be timestamped and saved to your selected directory.  
If "Split output" is enabled, each domain gets its own folder and file.

---

## 📃 License

MIT License — do whatever you want, but don't blame me if your firewall blocks you because you pasted 2000 URLs at once 😉
