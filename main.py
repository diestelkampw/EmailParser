import os
import re
import csv


def extract_emails_from_binary(target_domain, folder_path):
    unique_emails = set()
    # Matches strings that look like emails with your domain
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
                text_content = content.decode('utf-8', errors='ignore')

                # Find all matches for the domain
                matches = email_regex.findall(text_content)
                for addr in matches:
                    unique_emails.add(addr.lower())
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return sorted(list(unique_emails))


# --- Configuration ---
DOMAIN = "@army.mil"
# Use "." for the current directory or provide a specific path
MSG_FOLDER_PATH = "./MyEmailDump"
CSV_FILENAME = "extracted_emails.csv"

# --- Execution ---
results = extract_emails_from_binary(DOMAIN, MSG_FOLDER_PATH)

print(f"\n--- Found {len(results)} Unique Addresses ---")
for email in results:
    print(email)

# --- CSV Export Step ---
if results:
    try:
        # Get the current working directory to show the full path
        output_path = os.path.join(os.getcwd(), CSV_FILENAME)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Add a header row
            writer.writerow(["Email Address"])
            # Write the emails as individual rows
            for email in results:
                writer.writerow([email])

        print(f"\n[Success] CSV file created at: {output_path}")
    except Exception as e:
        print(f"\n[Error] Could not create CSV file: {e}")
else:
    print("\n[Notice] No emails found; CSV file was not created.")