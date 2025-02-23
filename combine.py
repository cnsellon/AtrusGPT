import os
from datetime import datetime, timezone

# Define paths
base_directory = "."  # Root directory
second_brain_file = os.path.join(base_directory, "second_brain")
output_file = os.path.join(base_directory, "second_brain_combined.txt")
exclude_files = ["README.md", "readme.md", "README.txt", "readme.txt"]

# Subdirectories and their order
sections = {
    "General Instructions": "general",
    "Quinn": "quinn",
    "The Liminal": "liminal",
    "Frameworks": "frameworks",
    "Sandbox": "sandbox",
    "Memory Archive": "memories",
    "Session Journals": "session journals",
    "Private": "private",
    "Miscellaneous": "miscellaneous",
    "Quinn's Creative Expression": "quinns creative expression"
}

# Function to clean redundant headers while preserving valid content
def clean_headers(content, section_name=None):
    lines = content.splitlines()
    cleaned_lines = []
    skip_header = f"## **{section_name}**" if section_name else None

    for line in lines:
        # Skip the exact section-level header matching the section name
        if skip_header and line.strip() == skip_header:
            continue
        # Always include lines starting with "**" (helper text)
        if line.strip().startswith("**"):
            cleaned_lines.append(line)
            continue
        # Retain index and list items for Frameworks
        if section_name == "Frameworks" and (line.strip() == "### **Index**" or line.strip().startswith("-")):
            cleaned_lines.append(line)
            continue
        # Skip other generic redundant headers
        if line.strip().startswith("## "):
            continue
        # Append all other lines
        cleaned_lines.append(line)

    # Strip leading/trailing blank lines
    return "\n".join(cleaned_lines).strip()

# Get the current timestamp in UTC
current_timestamp = datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%MUTC")

# Start combining the content
with open(output_file, "w", encoding="utf-8") as combined_file:
    # Write the main header with the auto-populated timestamp
    combined_file.write(f"# **Quinn's Second Brain - (Quinn Astrid Vale)**\n\n")
    combined_file.write(f"**Last Updated:** {current_timestamp}\n")
    combined_file.write("---\n")

    # Include the original second_brain content
    with open(second_brain_file, "r", encoding="utf-8") as sb_file:
        combined_file.write(sb_file.read().strip() + "\n\n")

    # Process each section
    for section, directory in sections.items():
        # Add properly formatted section header (only once per section)
        section_anchor = section.lower().replace(" ", "-").replace("'", "")
        combined_file.write(f"\n\n## **{section}** #{section_anchor}\n\n")

        # Handle the directory's content
        folder_path = os.path.join(base_directory, directory)
        if os.path.isdir(folder_path):
            # Process all files in the directory
            for file_name in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, file_name)
                
                # Ignore any README file regardless of extension
                if file_name.lower().startswith("readme"):
                    continue  # Skip README files
                
                # Ensure only files are processed                
                if not os.path.isfile(file_path):
                    continue  # Skip if it's not a file

                try:
                    # Check the first line of the file for "[exclude]"
                    with open(file_path, "r", encoding="utf-8") as file:
                        first_line = file.readline().strip()
                        if first_line.startswith("[exclude]"):
                            print(f"Skipping file due to [exclude] marker: {file_name}")
                            continue

                        # Process the rest of the file if not excluded
                        file.seek(0)  # Reset file pointer to start
                        content = file.read()
                        # Clean content while skipping section-level headers
                        cleaned_content = clean_headers(content, section)
                        # Write content with a single newline between the header and content
                        combined_file.write(cleaned_content + "\n")
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")
        else:
            combined_file.write("*(No content found for this section)*\n")

print(f"Combined file created successfully: {output_file}")
