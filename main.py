import os
import re


def extract_emails_from_binary(target_domain, folder_path):
    unique_emails = set()
    # Regex to find emails: looks for alphanumeric/dots + @yourdomain
    # We use [a-zA-Z0-9._%+-] to cover standard email characters
    regex_pattern = r'[a-zA-Z0-9._%+-]+' + re.escape(target_domain)
    email_regex = re.compile(regex_pattern, re.IGNORECASE)

    print(f"Scanning folder: {folder_path}")

    # List all files in the directory
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.msg')]
    print(f"Found {len(files)} .msg files to process...")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'rb') as f:
                # We read as binary ('rb') to avoid encoding crashes
                content = f.read()

                # Convert binary to string, ignoring characters it can't decode
                # This turns the binary "junk" into readable text strings
                text_content = content.decode('utf-8', errors='ignore')

                # Find all matches for @example.com
                matches = email_regex.findall(text_content)
                for addr in matches:
                    # Basic cleanup: some binary junk might attach to the start
                    clean_addr = addr.lower()
                    unique_emails.add(clean_addr)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return sorted(list(unique_emails))


# --- Configuration ---
DOMAIN = "@army.mil"
# Place the path to the folder where you dropped the .msg files
MSG_FOLDER_PATH = "./MyEmailDump"

results = extract_emails_from_binary(DOMAIN, MSG_FOLDER_PATH)

print(f"\n--- Found {len(results)} Unique Addresses ---")
for email in results:
    print(email)