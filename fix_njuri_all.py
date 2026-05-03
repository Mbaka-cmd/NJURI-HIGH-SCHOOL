"""
NJURI SENIOR SCHOOL — MASTER REPLACEMENT SCRIPT
================================================
Run this from your project root (same folder as manage.py):
    python fix_njuri_all.py

This script:
1. Replaces ALL Chuka Girls text with Njuri Senior School text
2. Fixes ALL colors from red to jungle green
3. Fixes navbar, footer, about, academics, every page
4. Works across all 65+ template files automatically
"""

import os
import re

# ── DIRECTORIES TO SCAN ───────────────────────────────────────────────────────
SCAN_DIRS = ["templates", "static"]
FILE_EXTENSIONS = [".html", ".css", ".js"]

# ── TEXT REPLACEMENTS ─────────────────────────────────────────────────────────
# Order matters — longer/more specific strings first
TEXT_REPLACEMENTS = [
    # School name variants
    ("St. Bakhita Chuka Girls High School",   "Njuri Senior School"),
    ("Chuka Girls Secondary School",           "Njuri Senior School"),
    ("Chuka Girls High School",                "Njuri Senior School"),
    ("St Bakhita Chuka Girls",                 "Njuri Senior School"),
    ("Chuka Girls",                            "Njuri Senior School"),
    ("chuka girls",                            "njuri senior school"),
    ("CHUKA GIRLS",                            "NJURI SENIOR SCHOOL"),
    ("chukagirls",                             "njurisenior"),
    ("ChukGirls",                              "NjuriSenior"),

    # Motto
    ("Virtue and Dignity",                     "Knowledge, Discipline and Service"),
    ("Virtue &amp; Dignity",                   "Knowledge, Discipline and Service"),

    # Contact details
    ("0115388019",                             "0722454131"),
    ("0115 388 019",                           "0722 454 131"),
    ("chukagirls@gmail.com",                   "njurihschool@yahoo.com"),
    ("official.mercymbaka@gmail.com",          "njurihschool@yahoo.com"),

    # Address
    ("Kiagondu Forest Road, Karingari, Chuka", "Magumoni Location, Meru South Sub-County"),
    ("Karingari, Chuka",                       "Meru South, Tharaka-Nithi"),
    ("Tharaka-Nithi County",                   "Tharaka-Nithi County"),  # keep same
    ("P.O. Box 3-60400",                       "P.O. Box 38, Magumoni 60403"),
    ("P.O Box 3-60400",                        "P.O. Box 38, Magumoni 60403"),

    # KNEC / codes
    ("19308304",                               "19308504"),
    ("KNEC: 19308304",                         "KNEC: 19308504"),

    # Principal
    ("Joan M. Muchina",                        "Rutere Henry Mwenda"),
    ("Joan Muthomi",                           "Rutere Henry Mwenda"),
    ("Joan Muchina",                           "Rutere Henry Mwenda"),
    ("Mrs. Joan",                              "Mr. Rutere"),

    # Category / type
    ("Extra County Girls Boarding",            "C2 Public Mixed Boarding"),
    ("Girls Boarding",                         "Mixed Boarding"),
    ("Girls Secondary",                        "Senior School"),
    ("girls school",                           "mixed school"),
    ("Girls School",                           "Mixed School"),

    # Hours / meta
    ("Mon-Fri: 8AM-5PM",                       "Mon-Fri: 8AM-5PM"),  # keep
    ("Mon–Fri: 8AM–5PM",                       "Mon–Fri: 8AM–5PM"),  # keep

    # URL slugs
    ("chuka-girls",                            "njuri-senior-school"),
    ("chuka_girls",                            "njuri_senior_school"),

    # Encoding artifacts (keep fixing these too)
   
]

# ── COLOR REPLACEMENTS ────────────────────────────────────────────────────────
COLOR_REPLACEMENTS = [
    # CSS hex colors — red to green
    ("#C0392B",          "#2D6A4F"),
    ("#c0392b",          "#2d6a4f"),
    ("#922B21",          "#1B4332"),
    ("#922b21",          "#1b4332"),
    ("#FDEDEC",          "#D8F3DC"),
    ("#fdedec",          "#d8f3dc"),
    ("#F9EBEA",          "#D8F3DC"),
    ("#f9ebea",          "#d8f3dc"),
    ("#E74C3C",          "#52B788"),
    ("#e74c3c",          "#52b788"),
    ("#CB4335",          "#2D6A4F"),
    ("#cb4335",          "#2d6a4f"),
    ("#B03A2E",          "#1B4332"),
    ("#b03a2e",          "#1b4332"),

    # CSS variable names
    ("--school-red:",    "--school-primary:"),
    ("--school-dark-red:", "--school-dark:"),
    ("var(--school-red)", "var(--school-primary)"),
    ("var(--school-dark-red)", "var(--school-dark)"),

    # Tailwind/Bootstrap red classes
    ("bg-danger",        "bg-success"),
    ("text-danger",      "text-success"),
    ("btn-danger",       "btn-success"),
    ("border-danger",    "border-success"),

    # Inline style colors
    ("color: #C0392B",   "color: #2D6A4F"),
    ("color:#C0392B",    "color:#2D6A4F"),
    ("color: #922B21",   "color: #1B4332"),
    ("color:#922B21",    "color:#1B4332"),
    ("background: #C0392B", "background: #2D6A4F"),
    ("background:#C0392B",  "background:#2D6A4F"),
    ("background-color: #C0392B", "background-color: #2D6A4F"),
    ("background-color:#C0392B",  "background-color:#2D6A4F"),
    ("background: #922B21",   "background: #1B4332"),
    ("background:#922B21",    "background:#1B4332"),
    ("border-color: #C0392B", "border-color: #2D6A4F"),
    ("border-color:#C0392B",  "border-color:#2D6A4F"),

    # Gradient patterns
    ("135deg, #C0392B",  "135deg, #2D6A4F"),
    ("135deg, #922B21",  "135deg, #1B4332"),
    ("#C0392B, #922B21", "#2D6A4F, #1B4332"),
    ("#922B21, #C0392B", "#1B4332, #2D6A4F"),
    ("#C0392B 0%",       "#1B4332 0%"),
    ("#922B21 0%",       "#1B4332 0%"),
    ("#C0392B)",         "#2D6A4F)"),
    ("#922B21)",         "#1B4332)"),

    # RGBA red variants
    ("rgba(192, 57, 43,", "rgba(45, 106, 79,"),
    ("rgba(146, 43, 33,", "rgba(27, 67, 50,"),
]

# ── NAVBAR SPECIFIC REPLACEMENTS ──────────────────────────────────────────────
NAVBAR_REPLACEMENTS = [
    # Title in navbar brand
    ("Chuka Girls Secondary School",  "Njuri Senior School"),
    ("Chuka Girls",                   "Njuri Senior School"),

    # Top bar contact info
    ("0115388019",                    "0722 454 131"),
    ("chukagirls@gmail.com",          "njurihschool@yahoo.com"),
    ("Kiagondu Forest Road, Karingari, Chuka", "Meru South Sub-County, Tharaka-Nithi"),

    # Meta tags
    ('content="Chuka Girls',          'content="Njuri Senior School'),
    ('content="St. Bakhita',          'content="Njuri Senior School'),
]

# ── ABOUT PAGE REPLACEMENTS ───────────────────────────────────────────────────
ABOUT_REPLACEMENTS = [
    ("1957",                           "1970"),  # founding year (update when known)
    ("Chuka, Tharaka-Nithi",          "Meru South, Tharaka-Nithi"),
    ("Extra County",                   "C2 Extra County"),
    ("KCSE 2024",                      "KCSE 2024"),  # keep
    ("133 candidates",                 "180 candidates"),
    ("mean grade B-",                  "mean grade C+"),
    ("mean grade of B-",               "mean grade of C+"),
    ("B minus",                        "C plus"),
    ("938 students",                   "925 students"),
    ("938",                            "925"),
    ("CGS",                            "NSS"),  # admission number prefix
]

# ── ACADEMIC YEAR DATA ────────────────────────────────────────────────────────
ACADEMIC_REPLACEMENTS = [
    ("Form 1 East",   "Form 1 North"),
    ("Form 1 West",   "Form 1 South"),
    ("Form 2 East",   "Form 2 North"),
    ("Form 2 West",   "Form 2 South"),
    ("Form 3 East",   "Form 3 North"),
    ("Form 3 West",   "Form 3 South"),
    ("Form 4 East",   "Form 4 North"),
    ("Form 4 West",   "Form 4 South"),
]

# ── MERGE ALL REPLACEMENTS ────────────────────────────────────────────────────
ALL_REPLACEMENTS = (
    TEXT_REPLACEMENTS +
    COLOR_REPLACEMENTS +
    NAVBAR_REPLACEMENTS +
    ABOUT_REPLACEMENTS +
    ACADEMIC_REPLACEMENTS
)

# ── SCRIPT RUNNER ─────────────────────────────────────────────────────────────
def fix_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            original = f.read()
    except Exception as e:
        print(f"  SKIP (read error): {filepath} — {e}")
        return 0

    content = original
    for old, new in ALL_REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            changes = sum(1 for old, _ in ALL_REPLACEMENTS if old in original)
            print(f"  FIXED ({changes} changes): {filepath}")
            return changes
        except Exception as e:
            print(f"  SKIP (write error): {filepath} — {e}")
            return 0
    return 0


def main():
    print("=" * 60)
    print("NJURI SENIOR SCHOOL — MASTER REPLACEMENT SCRIPT")
    print("=" * 60)
    print()

    total_files = 0
    total_changes = 0

    for scan_dir in SCAN_DIRS:
        if not os.path.exists(scan_dir):
            print(f"  Directory not found, skipping: {scan_dir}")
            continue

        print(f"Scanning: {scan_dir}/")
        for root, dirs, files in os.walk(scan_dir):
            # Skip venv and node_modules
            dirs[:] = [d for d in dirs if d not in ["venv", "node_modules", "__pycache__", ".git"]]
            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext in FILE_EXTENSIONS:
                    filepath = os.path.join(root, filename)
                    changes = fix_file(filepath)
                    if changes > 0:
                        total_files += 1
                        total_changes += changes

    print()
    print("=" * 60)
    print(f"DONE! Fixed {total_changes} items across {total_files} files.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. python manage.py migrate")
    print("  2. python manage.py create_admin")
    print("  3. python manage.py runserver")
    print("  4. Open http://127.0.0.1:8000")
    print("  5. Verify everything shows Njuri Senior School")
    print("  6. git add .")
    print('  7. git commit -m "Rebrand to Njuri Senior School"')
    print("  8. git push origin master")
    print()


if __name__ == "__main__":
    main()