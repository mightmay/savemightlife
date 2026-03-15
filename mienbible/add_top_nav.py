import os

# Hardcoded language data (using folder names as keys and display names)
navigation_data_hardcoded = {
    "MienLao": "Mien Lao Script",
    "MienNewRoman": "Mien New Roman Script",
    "ThaiMien": "Mien Thai Script",
    "WorldEnglishBible": "English"
}

def generate_simple_nav_bar_html(nav_data):
    html = """
    <style>
    .navbar {
        overflow: hidden;
        background-color: #333;
        font-family: Arial, sans-serif;
    }

    .navbar a {
        float: left;
        font-size: 16px;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }

    .navbar a:hover {
        background-color: #555;
    }
    </style>
    <div class="navbar">
        <a href="../../index.html">Home</a>
    """

    # Add language links
    for folder_name, display_name in nav_data.items():
        # Construct the link to the language's index.html
        language_index_link = f"../../{folder_name}/index.html"
        html += f'<a href="{language_index_link}">{display_name}</a>\n'

    html += "</div>"
    return html


def add_simple_nav_bar(directory, nav_html):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".htm"):
                filepath = os.path.join(root, file)
                print(f"Adding simple navigation bar to {filepath}...")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Find insertion point after the <body> tag
                    body_start = content.find('</head>')
                    if body_start != -1:
                        insertion_point = body_start + len('</head>')
                        modified_content = content[:insertion_point] + nav_html + content[insertion_point:]

                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(modified_content)
                        print(f"Added simple navigation bar to {filepath}")

                    else:
                        print(f"Could not find <body> tag in {filepath}. Skipping navigation insertion.")

                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

# Specify the directories you want to process
language_directories = ["MienLao", "MienNewRoman", "ThaiMien", "WorldEnglishBible"]

# Build navigation data (using hardcoded data)
navigation_data = navigation_data_hardcoded

# Generate simple navigation HTML
nav_html_content = generate_simple_nav_bar_html(navigation_data)

# Add simple navigation bar to HTML files
for lang_dir in language_directories:
     add_simple_nav_bar(lang_dir, nav_html_content)
