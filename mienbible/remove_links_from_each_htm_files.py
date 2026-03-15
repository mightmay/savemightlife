import os
import re

def remove_elements_by_class_and_id_regex(directory):
    # Patterns to look for the specific elements
    o11_pattern = re.compile(r'<div class="header" id="header">.*?</div>', re.DOTALL)
    o22_pattern = re.compile(r'<div class="linkNext">.*?</div>', re.DOTALL)
    o33_pattern = re.compile(r'<p class="footer">.*?</p>', re.DOTALL)

    header_div_pattern = re.compile(r'<form id="search" action="search/bibleSearch.php" method="post">.*?</form>', re.DOTALL)
    link_next_div_pattern = re.compile(r'<div class="linkPrev">.*?</div>', re.DOTALL)

    footer_p_pattern = re.compile(r'<p class="removeFootnotes" id="removeFootnotes">.*?</p>', re.DOTALL)
    footer_div_pattern = re.compile(r'<div class="footer" id="footer">.*?</div>', re.DOTALL) # Added pattern for footer div

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".htm"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    modified_content = content

                    # Remove the specific elements using regex
                    modified_content = re.sub(o11_pattern, '', modified_content)
                    modified_content = re.sub(o22_pattern, '', modified_content)
                    modified_content = re.sub(o33_pattern, '', modified_content)
                    
                    modified_content = re.sub(header_div_pattern, '', modified_content)
                    modified_content = re.sub(link_next_div_pattern, '', modified_content)
                    modified_content = re.sub(footer_p_pattern, '', modified_content)
                    modified_content = re.sub(footer_div_pattern, '', modified_content) # Added removal for footer div

                    # Write the modified content back to the file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    print(f"Removed specified elements from {filepath}")

                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

# Specify the directories you want to process
language_directories = ["MienLao", "MienNewRoman", "ThaiMien", "WorldEnglishBible"]

# Remove specific elements from HTML files using regex
for lang_dir in language_directories:
    remove_elements_by_class_and_id_regex(lang_dir)
