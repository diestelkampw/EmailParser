readme_content = """# Email Domain Extractor (OS-Agnostic)

A lightweight, zero-dependency Python script designed for restricted corporate environments. This tool extracts unique email addresses belonging to a specific domain from Outlook message files (`.msg`) and email files (`.eml`).

## The Problem
In high-security environments (with SSO, Okta, and Hardware Validation like BeyondIdentity), scripts often cannot authenticate directly with mail servers via IMAP. Additionally, corporate laptops often restrict the installation of third-party Python libraries (like `extract-msg` or `pywin32`).

## The Solution
This script uses **Raw Binary Scraping**. It doesn't "open" the email file in the traditional sense; instead, it scans the file's raw data for strings that match your target domain. 

- **No Admin Rights Required:** Runs with standard user permissions.
- **Zero Dependencies:** Uses only built-in Python libraries (`os`, `re`, `csv`).
- **OS-Agnostic:** Works on Windows and macOS.
- **Privacy First:** All processing happens locally on your machine.

---

## How to Use

### 1. Gather your Data
1. Open **Outlook**.
2. Perform a **Global Search** (All Outlook Items) for your target domain (e.g., `@example.com`).
3. Select the results (`Ctrl+A` or `Cmd+A`).
4. **Drag and Drop** the selected emails into a new folder on your desktop (e.g., `MyEmails`).

### 2. Configure the Script
Open the script in any text editor and update the variables at the bottom of the file:
- `DOMAIN`: The domain you are looking for (e.g., `@example.com`).
- `MSG_FOLDER_PATH`: The path to the folder containing your exported `.msg` or `.eml` files.

### 3. Run the Script
Open your terminal or PowerShell and run:
```bash
python scrape_emails.py
