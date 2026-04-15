import os
import re
from email import policy
from email.parser import BytesParser


def extract_emails(target_domain, folder_path):
    unique_emails = set()
    # Matches standard email patterns
    email_regex = re.compile(r'[\w\.-]+' + re.escape(target_domain), re.IGNORECASE)

    print(f"Scanning files in: {folder_path}...")

    for filename in os.listdir(folder_path):
        if filename.endswith(".eml") or filename.endswith(".msg"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'rb') as f:
                    # Parse the email file
                    msg = BytesParser(policy=policy.default).parse(f)

                    # Consolidate headers to search
                    headers_to_search = [
                        msg.get('To', ''),
                        msg.get('From', ''),
                        msg.get('Cc', ''),
                        msg.get('Bcc', '')
                    ]

                    for header in headers_to_search:
                        matches = email_regex.findall(str(header))
                        for email in matches:
                            unique_emails.add(email.lower())
            except Exception as e:
                print(f"Could not read {filename}: {e}")

    return sorted(list(unique_emails))


# --- Configuration ---
DOMAIN = "@army.mil"
# Use "." for current directory or provide a path
PATH_TO_EMAILS = "./my_emails"

results = extract_emails(DOMAIN, PATH_TO_EMAILS)

print(f"\n--- Found {len(results)} Unique Emails ---")
for email in results:
    print(email)