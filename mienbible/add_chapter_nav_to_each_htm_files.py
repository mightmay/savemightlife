import os

def add_navigation_to_html(directory):
    # Define the correct order of books
    book_order = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
        "Ruth", "1Samuel", "2Samuel", "1Kings", "2Kings", "1Chronicles", "2Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes",
        "SongOfSolomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
        "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke",
        "John", "Acts", "Romans", "1Corinthians", "2Corinthians", "Galatians",
        "Ephesians", "Philippians", "Colossians", "1Thessalonians", "2Thessalonians",
        "1Timothy", "2Timothy", "Titus", "Philemon", "Hebrews", "James", "1Peter",
        "2Peter", "1John", "2John", "3John", "Jude", "Revelation"
    ]

    # CSS block for our buttons + hover state
    style_block = """
    <style>
    .chapter-navigation a {
        display: inline-block;
        background-color: #4CAF50;
        color: #fff;
        font-weight: bold;
        font-size: 1em;
        text-decoration: none;
        padding: 10px 16px;
        margin: 8px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .chapter-navigation a:hover {
        background-color: #45a049;
    }
    </style>
    """

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".htm"):
                continue

            filepath = os.path.join(root, file)
            print(f"Processing {filepath}...")

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Derive language, book and chapter from path
            parts = filepath.split(os.sep)
            if len(parts) < 3:
                print(f"  ↳ Cannot parse path segments, skipping.")
                continue

            language_name = parts[-3]
            book_name     = parts[-2]
            chapter_str   = os.path.splitext(parts[-1])[0]
            if not chapter_str.isdigit():
                print(f"  ↳ Filename '{chapter_str}' is not a chapter number, skipping.")
                continue

            current = int(chapter_str)
            book_dir = os.path.join(root)
            chapter_files = sorted(
                [c for c in os.listdir(book_dir)
                 if c.endswith(".htm") and os.path.splitext(c)[0].isdigit()],
                key=lambda x: int(os.path.splitext(x)[0])
            )

            if not chapter_files:
                print(f"  ↳ No numeric .htm chapters found in '{book_dir}'.")
                continue

            first_chap = int(os.path.splitext(chapter_files[0])[0])
            last_chap  = int(os.path.splitext(chapter_files[-1])[0])

            # Build prev/next links
            prev_link = ""
            next_link = ""

            # Previous chapter or book
            if current > first_chap:
                prev_link = f'<a href="../{book_name}/{current-1}.htm">&lt;– Previous</a>'
            else:
                # jump to last of previous book
                lang_dir = os.path.dirname(book_dir)
                available = [b for b in book_order if os.path.isdir(os.path.join(lang_dir, b))]
                if book_name in available:
                    idx = available.index(book_name)
                    if idx > 0:
                        prev_book = available[idx-1]
                        prev_chaps = sorted(
                            [c for c in os.listdir(os.path.join(lang_dir, prev_book))
                             if c.endswith(".htm") and os.path.splitext(c)[0].isdigit()],
                            key=lambda x: int(os.path.splitext(x)[0])
                        )
                        if prev_chaps:
                            num = os.path.splitext(prev_chaps[-1])[0]
                            prev_link = (
                                f'<a href="../../{language_name}/{prev_book}/{num}.htm">'
                                f"&lt;– {prev_book} {num}</a>"
                            )

            # Next chapter or book
            if current < last_chap:
                next_link = f'<a href="../{book_name}/{current+1}.htm">Next –&gt;</a>'
            else:
                lang_dir = os.path.dirname(book_dir)
                available = [b for b in book_order if os.path.isdir(os.path.join(lang_dir, b))]
                if book_name in available:
                    idx = available.index(book_name)
                    if idx < len(available)-1:
                        next_book = available[idx+1]
                        next_chaps = sorted(
                            [c for c in os.listdir(os.path.join(lang_dir, next_book))
                             if c.endswith(".htm") and os.path.splitext(c)[0].isdigit()],
                            key=lambda x: int(os.path.splitext(x)[0])
                        )
                        if next_chaps:
                            num = os.path.splitext(next_chaps[0])[0]
                            next_link = (
                                f'<a href="../../{language_name}/{next_book}/{num}.htm">'
                                f"{next_book} {num} –&gt;</a>"
                            )

            nav_div = (
                '<div class="chapter-navigation" '
                'style="text-align:center; margin:20px 0;">'
                f"{prev_link}&nbsp;&nbsp;&nbsp;{next_link}"
                "</div>"
            )

            # Inject style + navigation after </head>, fallback into <body>
            head_end = content.find("</head>")
            if head_end != -1:
                insertion = style_block + nav_div
                new_content = (
                    content[:head_end+7] +
                    insertion +
                    content[head_end+7:]
                )
            else:
                body_start = content.find("<body>")
                if body_start != -1:
                    insertion = style_block + nav_div
                    new_content = (
                        content[:body_start+6] +
                        insertion +
                        content[body_start+6:]
                    )
                else:
                    print(f"  ↳ No <head> or <body> tag found, skipping.")
                    continue
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  ✔ Navigation injected into {filepath}")
            except Exception as e:
                print(f"  ✘ Failed to write {filepath}: {e}")
                continue
    
# Run across your language folders
for lang in ["MienLao", "MienNewRoman", "ThaiMien", "WorldEnglishBible"]:
    add_navigation_to_html(lang)
