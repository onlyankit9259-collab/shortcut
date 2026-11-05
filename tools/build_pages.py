#!/usr/bin/env python3
"""Generate the category pages (ms-word-shortcuts.html, ...) and sitemap.xml.

Edit the PAGES data below, then run:
  python3 tools/build_pages.py
Each page gets its own title and description so Google can show it for
searches like "MS Word shortcut keys in Hindi".
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://onlyankit9259-collab.github.io/shortcut/"
YOUTUBE = "https://youtube.com/@shortcutguru_sg"
INSTAGRAM = "https://www.instagram.com/shortcutguru_sg/"
LASTMOD = "2026-11-05"

# Each table: title, optional howto (HTML), column names, rows.
# A row is (copy text, what it does[, extra column]).
PAGES = [
    {
        "file": "ms-word-shortcuts.html",
        "nav": "MS Word",
        "emoji": "📝",
        "title": "MS Word Shortcut Keys in Hindi – 40+ Keyboard Shortcuts | Shortcut Guru",
        "h1": "MS Word <span>Shortcut Keys</span> in Hindi",
        "description": "MS Word ke 40+ zaroori keyboard shortcut keys Hindi mein: Bold, Copy, Paste, Page Break, Font size, Spelling check aur bahut kuch. Search karo aur ek click mein copy karo.",
        "intro": "MS Word mein mouse ki jagah keyboard use karke apna kaam 2 guna tez karo. Yeh sabhi shortcuts Word 2010, 2016, 2019, 2021 aur Microsoft 365 mein chalte hain.",
        "tables": [{
            "title": "MS Word Keyboard Shortcuts",
            "cols": ["Shortcut", "Kya hota hai"],
            "rows": [
                ("Ctrl + A", "Poora document select karo"),
                ("Ctrl + B", "Text ko Bold karo"),
                ("Ctrl + I", "Text ko Italic (tircha) karo"),
                ("Ctrl + U", "Text ke neeche Underline lagao"),
                ("Ctrl + C", "Selected text Copy karo"),
                ("Ctrl + X", "Selected text Cut karo"),
                ("Ctrl + V", "Copy/Cut kiya text Paste karo"),
                ("Ctrl + Z", "Pichla kaam Undo karo"),
                ("Ctrl + Y", "Undo kiya kaam wapas lao (Redo)"),
                ("Ctrl + S", "Document Save karo"),
                ("F12", "Save As – naye naam se save karo"),
                ("Ctrl + N", "Naya blank document kholo"),
                ("Ctrl + O", "Purana document kholo (Open)"),
                ("Ctrl + W", "Document band karo"),
                ("Ctrl + P", "Print ya PDF save karo"),
                ("Ctrl + F", "Document mein shabd dhoondo (Find)"),
                ("Ctrl + H", "Shabd dhoond kar badlo (Replace)"),
                ("Ctrl + G", "Kisi page number par jao (Go To)"),
                ("Ctrl + E", "Text ko Center mein lao"),
                ("Ctrl + L", "Text ko Left align karo"),
                ("Ctrl + R", "Text ko Right align karo"),
                ("Ctrl + J", "Text ko Justify karo (dono taraf barabar)"),
                ("Ctrl + M", "Paragraph ka Indent badhao"),
                ("Ctrl + Shift + M", "Paragraph ka Indent kam karo"),
                ("Ctrl + 1", "Single line spacing"),
                ("Ctrl + 2", "Double line spacing"),
                ("Ctrl + 5", "1.5 line spacing"),
                ("Ctrl + Shift + >", "Font size bada karo"),
                ("Ctrl + Shift + <", "Font size chhota karo"),
                ("Ctrl + ]", "Font size 1 point badhao"),
                ("Ctrl + [", "Font size 1 point ghatao"),
                ("Ctrl + D", "Font dialog box kholo"),
                ("Shift + F3", "Capital/small letters badlo (Change Case)"),
                ("Ctrl + =", "Subscript (H₂O jaisa)"),
                ("Ctrl + Shift + =", "Superscript (x² jaisa)"),
                ("Ctrl + K", "Hyperlink (link) lagao"),
                ("Ctrl + Enter", "Naya page shuru karo (Page Break)"),
                ("Ctrl + Home", "Document ki shuruaat par jao"),
                ("Ctrl + End", "Document ke aakhir mein jao"),
                ("F7", "Spelling aur Grammar check karo"),
                ("Alt + Shift + D", "Aaj ki date daalo"),
                ("Alt + Shift + T", "Abhi ka time daalo"),
                ("Alt + X", "Code ko emoji/symbol mein badlo (jaise 1F980 → 🦀)"),
            ],
        }],
    },
    {
        "file": "ms-excel-shortcuts.html",
        "nav": "MS Excel",
        "emoji": "📊",
        "title": "MS Excel Shortcut Keys in Hindi – 40+ Keyboard Shortcuts | Shortcut Guru",
        "h1": "MS Excel <span>Shortcut Keys</span> in Hindi",
        "description": "MS Excel ke 40+ zaroori shortcut keys Hindi mein: AutoSum, Format Cells, Filter, Date, Flash Fill, Sheet badalna aur bahut kuch. Search karo aur copy karo.",
        "intro": "Excel mein data entry, total aur formatting ka kaam shortcuts se minto ki jagah second mein hota hai. Office jobs aur computer course ke liye yeh shortcuts zaroor yaad karo.",
        "tables": [{
            "title": "MS Excel Keyboard Shortcuts",
            "cols": ["Shortcut", "Kya hota hai"],
            "rows": [
                ("Ctrl + C", "Cell Copy karo"),
                ("Ctrl + X", "Cell Cut karo"),
                ("Ctrl + V", "Paste karo"),
                ("Ctrl + Z", "Undo karo"),
                ("Ctrl + Y", "Redo karo"),
                ("Ctrl + S", "Workbook Save karo"),
                ("Ctrl + A", "Poori sheet / table select karo"),
                ("Ctrl + F", "Data dhoondo (Find)"),
                ("Ctrl + H", "Dhoond kar badlo (Replace)"),
                ("Ctrl + B", "Bold karo"),
                ("Ctrl + I", "Italic karo"),
                ("Ctrl + U", "Underline karo"),
                ("F2", "Active cell ko edit karo"),
                ("Alt + =", "AutoSum – column ka total ek click mein"),
                ("Ctrl + 1", "Format Cells box kholo"),
                ("Ctrl + ;", "Aaj ki date daalo"),
                ("Ctrl + Shift + ;", "Abhi ka time daalo"),
                ("Alt + Enter", "Ek hi cell mein nayi line"),
                ("Ctrl + D", "Upar wale cell ko neeche copy karo (Fill Down)"),
                ("Ctrl + R", "Left wale cell ko right copy karo (Fill Right)"),
                ("Ctrl + E", "Flash Fill – pattern dekh kar data khud bharo"),
                ("Ctrl + Space", "Poora column select karo"),
                ("Shift + Space", "Poori row select karo"),
                ("Ctrl + Shift + +", "Nayi row/column/cell insert karo"),
                ("Ctrl + -", "Row/column/cell delete karo"),
                ("Ctrl + Shift + L", "Filter on/off karo"),
                ("Ctrl + T", "Data ko Table banao"),
                ("F4", "Formula mein $ lagao (Absolute reference) / pichla kaam dohraao"),
                ("Ctrl + `", "Saare formulas dikhao"),
                ("Ctrl + Arrow key", "Data ke aakhri cell tak jao"),
                ("Ctrl + Shift + Arrow key", "Data ke aakhir tak select karo"),
                ("Ctrl + Home", "Cell A1 par jao"),
                ("Ctrl + End", "Data ke aakhri cell par jao"),
                ("Ctrl + Page Down", "Agli sheet par jao"),
                ("Ctrl + Page Up", "Pichli sheet par jao"),
                ("Shift + F11", "Nayi sheet banao"),
                ("Ctrl + Shift + $", "Number ko Currency format do"),
                ("Ctrl + Shift + %", "Number ko Percentage format do"),
                ("Alt + F1", "Selected data ka Chart banao"),
                ("F11", "Nayi sheet par Chart banao"),
                ("Ctrl + 9", "Row chhupao (Hide)"),
                ("Ctrl + 0", "Column chhupao (Hide)"),
            ],
        }],
    },
    {
        "file": "windows-shortcuts.html",
        "nav": "Windows",
        "emoji": "🪟",
        "title": "Windows 10 & 11 Shortcut Keys in Hindi – 35+ Keyboard Tricks | Shortcut Guru",
        "h1": "Windows 10 &amp; 11 <span>Shortcut Keys</span> in Hindi",
        "description": "Windows 10 aur Windows 11 ke 35+ kaam ke shortcut keys Hindi mein: Screenshot, Clipboard history, Emoji panel, Lock, Task Manager, Screen recording aur bahut kuch.",
        "intro": "Win key (⊞ Windows logo wali key) ke saath yeh shortcuts aapke laptop aur computer ko tez chalane mein madad karte hain. Zyadatar Windows 10 aur 11 dono mein chalte hain.",
        "tables": [{
            "title": "Windows Keyboard Shortcuts",
            "cols": ["Shortcut", "Kya hota hai"],
            "rows": [
                ("Win", "Start menu kholo"),
                ("Win + D", "Seedha Desktop dikhao / wapas lao"),
                ("Win + E", "File Explorer kholo"),
                ("Win + L", "Computer Lock karo"),
                ("Win + I", "Settings kholo"),
                ("Win + R", "Run box kholo"),
                ("Win + S", "Search kholo"),
                ("Win + V", "Clipboard history – pehle copy kiye items dekho"),
                ("Win + .", "Emoji panel kholo 😀"),
                ("Win + Shift + S", "Screen ka hissa screenshot lo (Snipping)"),
                ("Win + PrtScn", "Poori screen ka screenshot Pictures mein save karo"),
                ("PrtScn", "Poori screen ka screenshot copy karo"),
                ("Win + Alt + R", "Screen recording shuru/band karo (Game Bar)"),
                ("Win + G", "Xbox Game Bar kholo"),
                ("Win + H", "Bol kar type karo (Voice typing)"),
                ("Alt + Tab", "Khule apps ke beech switch karo"),
                ("Win + Tab", "Task View – saare windows aur desktops dekho"),
                ("Alt + F4", "Khula app/window band karo"),
                ("Ctrl + Shift + Esc", "Task Manager seedha kholo"),
                ("Win + M", "Saari windows minimize karo"),
                ("Win + ↑", "Window ko maximize karo"),
                ("Win + ← / →", "Window ko screen ke aadhe hisse mein lagao (Snap)"),
                ("Win + Ctrl + D", "Naya virtual desktop banao"),
                ("Win + Ctrl + ← / →", "Virtual desktops ke beech jao"),
                ("Win + P", "Projector / dusri screen ka mode chuno"),
                ("Win + A", "Quick Settings (Wi-Fi, Bluetooth) kholo"),
                ("Win + N", "Notifications aur calendar kholo (Windows 11)"),
                ("Win + K", "TV / wireless display par cast karo"),
                ("Win + X", "Power user menu (Device Manager, Disk) kholo"),
                ("Win + +", "Magnifier se screen zoom karo"),
                ("F2", "Selected file ka naam badlo (Rename)"),
                ("Ctrl + Shift + N", "Nayi folder banao"),
                ("Shift + Delete", "File ko Recycle Bin ke bina hamesha ke liye delete karo"),
                ("Alt + Enter", "Selected file ki Properties dekho"),
                ("Win + Ctrl + Shift + B", "Display driver restart karo (screen atak jaye to)"),
            ],
        }],
    },
    {
        "file": "chrome-shortcuts.html",
        "nav": "Chrome",
        "emoji": "🌐",
        "title": "Google Chrome Shortcut Keys in Hindi – 30+ Browser Shortcuts | Shortcut Guru",
        "h1": "Google Chrome <span>Shortcut Keys</span> in Hindi",
        "description": "Google Chrome ke 30+ shortcut keys Hindi mein: band tab wapas kholo, Incognito, History, Downloads, Zoom, Page ko PDF save karo aur bahut kuch.",
        "intro": "Browser mein roz ka kaam – tab kholna, band karna, history saaf karna – yeh sab keyboard se aur tez hota hai. Yeh shortcuts Microsoft Edge mein bhi chalte hain.",
        "tables": [{
            "title": "Chrome Keyboard Shortcuts",
            "cols": ["Shortcut", "Kya hota hai"],
            "rows": [
                ("Ctrl + T", "Naya tab kholo"),
                ("Ctrl + Shift + T", "Galti se band hua tab wapas kholo"),
                ("Ctrl + W", "Abhi wala tab band karo"),
                ("Ctrl + N", "Nayi window kholo"),
                ("Ctrl + Shift + N", "Incognito window kholo"),
                ("Ctrl + Tab", "Agle tab par jao"),
                ("Ctrl + Shift + Tab", "Pichle tab par jao"),
                ("Ctrl + 1 to 8", "Us number wale tab par jao"),
                ("Ctrl + 9", "Aakhri tab par jao"),
                ("Ctrl + L", "Address bar select karo"),
                ("Ctrl + Enter", "Address bar mein www. aur .com khud lagao"),
                ("Ctrl + D", "Page ko Bookmark karo"),
                ("Ctrl + Shift + B", "Bookmarks bar dikhao/chhupao"),
                ("Ctrl + H", "History kholo"),
                ("Ctrl + J", "Downloads kholo"),
                ("Ctrl + Shift + Delete", "Browsing data / history saaf karo"),
                ("Ctrl + F", "Page mein shabd dhoondo"),
                ("Ctrl + R", "Page reload karo"),
                ("Ctrl + Shift + R", "Cache ke bina reload karo (Hard reload)"),
                ("Ctrl + +", "Zoom in karo"),
                ("Ctrl + -", "Zoom out karo"),
                ("Ctrl + 0", "Zoom normal karo"),
                ("F11", "Full screen karo"),
                ("Ctrl + P", "Print karo / page ko PDF save karo"),
                ("Ctrl + S", "Page save karo"),
                ("Ctrl + U", "Page ka source code dekho"),
                ("F12", "Developer Tools kholo"),
                ("Alt + ←", "Pichle page par jao (Back)"),
                ("Alt + →", "Agle page par jao (Forward)"),
                ("Space", "Page neeche scroll karo"),
                ("Shift + Space", "Page upar scroll karo"),
                ("Esc", "Page loading rok do"),
            ],
        }],
    },
    {
        "file": "vscode-shortcuts.html",
        "nav": "VS Code",
        "emoji": "👨‍💻",
        "title": "VS Code Shortcut Keys in Hindi – 30+ Coding Shortcuts | Shortcut Guru",
        "h1": "VS Code <span>Shortcut Keys</span> in Hindi",
        "description": "Visual Studio Code ke 30+ shortcut keys Hindi mein: Command Palette, Multi-cursor, Line move/copy, Format document, Terminal aur bahut kuch. Coding tez karo.",
        "intro": "Coding seekh rahe ho? Yeh VS Code shortcuts har programmer roz use karta hai – HTML, CSS, JavaScript, Python sab ke liye kaam aate hain. (Windows keyboard ke liye)",
        "tables": [{
            "title": "VS Code Keyboard Shortcuts",
            "cols": ["Shortcut", "Kya hota hai"],
            "rows": [
                ("Ctrl + Shift + P", "Command Palette – har command yahan se"),
                ("Ctrl + P", "File ka naam likh kar jaldi kholo (Quick Open)"),
                ("Ctrl + S", "File save karo"),
                ("Ctrl + Shift + N", "Nayi VS Code window"),
                ("Ctrl + W", "Khuli file band karo"),
                ("Ctrl + Tab", "Khuli files ke beech switch karo"),
                ("Ctrl + \\", "Editor ko do hisson mein baanto (Split)"),
                ("Ctrl + B", "Sidebar dikhao/chhupao"),
                ("Ctrl + Shift + E", "Explorer kholo"),
                ("Ctrl + Shift + F", "Saari files mein search karo"),
                ("Ctrl + Shift + X", "Extensions kholo"),
                ("Ctrl + Shift + G", "Source Control (Git) kholo"),
                ("Ctrl + `", "Terminal kholo/band karo"),
                ("Ctrl + ,", "Settings kholo"),
                ("Ctrl + /", "Line ko comment / uncomment karo"),
                ("Shift + Alt + A", "Block comment lagao"),
                ("Alt + ↑", "Line ko upar le jao"),
                ("Alt + ↓", "Line ko neeche le jao"),
                ("Shift + Alt + ↓", "Line ki copy neeche banao"),
                ("Ctrl + Shift + K", "Poori line delete karo"),
                ("Ctrl + Enter", "Neeche nayi line banao"),
                ("Ctrl + D", "Agla same shabd bhi select karo"),
                ("Ctrl + Shift + L", "Same shabd ke saare match select karo"),
                ("Alt + Click", "Kai jagah ek saath cursor lagao (Multi-cursor)"),
                ("Ctrl + Alt + ↓", "Neeche wali line par bhi cursor lagao"),
                ("Shift + Alt + F", "Poora code format karo (Format Document)"),
                ("Ctrl + Space", "Suggestions dikhao"),
                ("F2", "Variable ka naam har jagah badlo (Rename)"),
                ("F12", "Function ki definition par jao"),
                ("Ctrl + G", "Line number par jao"),
                ("Ctrl + F", "File mein dhoondo"),
                ("Ctrl + H", "File mein dhoond kar badlo"),
                ("F5", "Debugging shuru karo"),
            ],
        }],
    },
    {
        "file": "cmd-commands.html",
        "nav": "CMD",
        "emoji": "🖥️",
        "title": "CMD Commands & Tricks in Hindi – 30+ Command Prompt Commands | Shortcut Guru",
        "h1": "CMD <span>Commands &amp; Tricks</span> in Hindi",
        "description": "Windows Command Prompt (CMD) ke 30+ kaam ke commands aur hacker-look tricks Hindi mein: ipconfig, ping, Wi-Fi password dekhna, systeminfo, color 0a, tree aur bahut kuch.",
        "intro": "CMD kholne ke liye Win + R dabao, cmd likho aur Enter dabao. Neeche diye commands copy karke CMD mein paste karo (Ctrl + V ya right click). Yeh sab safe commands hain.",
        "tables": [
            {
                "title": "😎 Hacker Look Tricks",
                "cols": ["Command", "Kya hota hai"],
                "rows": [
                    ("color 0a", "Kaali screen par hara text – hacker look"),
                    ("color 0c", "Kaali screen par laal text"),
                    ("color 07", "Normal rang wapas lao"),
                    ("title Shortcut Guru", "CMD window ka naam badlo"),
                    ("tree", "Folders ka ped (tree) chalta hua dikhao"),
                    ("dir /s", "Saari files ki lambi list scroll hoti dikhegi"),
                    ("echo Hello Shortcut Guru", "Screen par apna message likho"),
                    ("cls", "Screen saaf karo"),
                ],
            },
            {
                "title": "🛠️ Kaam ke Commands",
                "cols": ["Command", "Kya hota hai"],
                "rows": [
                    ("ipconfig", "Apna IP address dekho"),
                    ("ping google.com", "Internet chal raha hai ya nahi, check karo"),
                    ("netsh wlan show profiles", "Is computer par save Wi-Fi ke naam dekho"),
                    ("netsh wlan show profile name=\"WiFiName\" key=clear", "Apne save Wi-Fi ka password dekho (WiFiName ki jagah naam likho)"),
                    ("systeminfo", "Computer ki poori jaankari (RAM, Windows version)"),
                    ("ver", "Windows ka version dekho"),
                    ("hostname", "Computer ka naam dekho"),
                    ("whoami", "Abhi login user ka naam dekho"),
                    ("tasklist", "Chal rahe saare programs ki list"),
                    ("taskkill /im notepad.exe /f", "Atka hua program band karo (notepad.exe ki jagah program ka naam)"),
                    ("date", "Date dekho / badlo"),
                    ("time", "Time dekho / badlo"),
                    ("dir", "Folder ki files aur folders dekho"),
                    ("cd ..", "Ek folder peeche jao"),
                    ("cd Desktop", "Desktop folder mein jao"),
                    ("mkdir MyFolder", "Nayi folder banao"),
                    ("start notepad", "Notepad kholo"),
                    ("start calc", "Calculator kholo"),
                    ("shutdown /s /t 60", "60 second baad computer band karo"),
                    ("shutdown /a", "Shutdown cancel karo"),
                    ("shutdown /r /t 0", "Computer turant restart karo"),
                    ("sfc /scannow", "Windows ki kharab files theek karo (Admin CMD mein)"),
                    ("help", "Saare commands ki list"),
                    ("exit", "CMD band karo"),
                ],
            },
        ],
    },
]

ALT_CODES = [
    ("☺", "Alt + 1", "Smiley"), ("☻", "Alt + 2", "Black smiley"), ("♥", "Alt + 3", "Heart"),
    ("♦", "Alt + 4", "Diamond"), ("♣", "Alt + 5", "Club"), ("♠", "Alt + 6", "Spade"),
    ("♂", "Alt + 11", "Male"), ("♀", "Alt + 12", "Female"), ("♪", "Alt + 13", "Music note"),
    ("♫", "Alt + 14", "Music notes"), ("☼", "Alt + 15", "Sun"), ("►", "Alt + 16", "Right arrow"),
    ("◄", "Alt + 17", "Left arrow"), ("↑", "Alt + 24", "Up arrow"), ("↓", "Alt + 25", "Down arrow"),
    ("→", "Alt + 26", "Right arrow"), ("←", "Alt + 27", "Left arrow"), ("▲", "Alt + 30", "Up triangle"),
    ("▼", "Alt + 31", "Down triangle"), ("⌂", "Alt + 127", "House"), ("¢", "Alt + 155", "Cent"),
    ("£", "Alt + 156", "Pound"), ("¥", "Alt + 157", "Yen"), ("€", "Alt + 0128", "Euro"),
    ("½", "Alt + 171", "Half"), ("¼", "Alt + 172", "Quarter"), ("░", "Alt + 176", "Light shade"),
    ("▒", "Alt + 177", "Medium shade"), ("▓", "Alt + 178", "Dark shade"), ("█", "Alt + 219", "Full block"),
    ("■", "Alt + 254", "Square"), ("∞", "Alt + 236", "Infinity"), ("±", "Alt + 241", "Plus minus"),
    ("÷", "Alt + 246", "Divide"), ("×", "Alt + 0215", "Multiply"), ("≈", "Alt + 247", "Almost equal"),
    ("°", "Alt + 248", "Degree"), ("√", "Alt + 251", "Square root"), ("²", "Alt + 253", "Square (power 2)"),
    ("©", "Alt + 0169", "Copyright"), ("®", "Alt + 0174", "Registered"), ("™", "Alt + 0153", "Trademark"),
]
WORD_EMOJI = [
    ("🦀", "1F980", "Crab"), ("🦅", "1F985", "Eagle"), ("🦟", "1F99F", "Mosquito"),
    ("🦋", "1F98B", "Butterfly"), ("🐜", "1F41C", "Ant"), ("🦜", "1F99C", "Parrot"),
    ("🐒", "1F412", "Monkey"), ("🎂", "1F382", "Cake"), ("✈", "2708", "Aeroplane"),
    ("🏠", "1F3E0", "House"), ("🏆", "1F3C6", "Trophy"), ("🔦", "1F526", "Torch"),
    ("🚀", "1F680", "Rocket"), ("🚴", "1F6B4", "Cycle"), ("🏥", "1F3E5", "Hospital"),
    ("🌍", "1F30D", "Earth"), ("🗺", "1F5FA", "World map"), ("❄", "2744", "Snow"),
    ("❤", "2764", "Heart"), ("⭐", "2B50", "Star"), ("🔥", "1F525", "Fire"),
    ("💻", "1F4BB", "Laptop"), ("🪔", "1FA94", "Diya"),
]
PAGES.append({
    "file": "alt-codes.html",
    "nav": "Alt Codes",
    "emoji": "🦀",
    "title": "Alt Codes List & MS Word Emoji Codes in Hindi (Alt + X) | Shortcut Guru",
    "h1": "Alt Codes &amp; <span>Keyboard Emoji</span> Codes",
    "description": "Keyboard se symbols aur emoji banao: 40+ Windows Alt codes (♥ © ° √ →) aur MS Word Alt + X emoji codes (🦀 1F980, 🦅 1F985, 🚀 1F680). Hindi mein tarika aur copy button.",
    "intro": "Hamare YouTube Shorts wale saare keyboard emoji codes yahan hain. Symbol copy karo ya code se khud banao.",
    "tables": [
        {
            "title": "Windows Alt Codes",
            "howto": "<b>Kaise use karein:</b> <kbd>Alt</kbd> daba kar rakho, number pad (right side wale number) se code likho, phir <kbd>Alt</kbd> chhod do. Laptop mein number pad nahi hai to <kbd>Fn</kbd> / <kbd>Num Lock</kbd> on karo.",
            "cols": ["Symbol", "Alt Code", "Name"],
            "symbol": True,
            "rows": ALT_CODES,
        },
        {
            "title": "MS Word Emoji Codes (Alt + X)",
            "howto": "<b>MS Word mein:</b> code type karo (jaise <kbd>1F980</kbd>), phir turant <kbd>Alt</kbd> + <kbd>X</kbd> dabao – code emoji ban jayega 🦀. Yahi trick hamare YouTube Shorts mein hai!",
            "cols": ["Emoji", "Word Code", "Name"],
            "symbol": True,
            "rows": [(e, c + " → Alt + X", n) for e, c, n in WORD_EMOJI],
        },
    ],
})


def esc(text):
    return html.escape(text, quote=True)


def nav_html(current):
    links = ['  <a href="./">Home</a>']
    for p in PAGES:
        attr = ' aria-current="page"' if p["file"] == current else ""
        links.append(f'  <a href="{p["file"]}"{attr}>{p["nav"]}</a>')
    links.append('  <a href="./#pdfs">PDF Notes</a>')
    return "\n".join(links)


def table_html(t, i):
    head = "".join(f"<th>{esc(c)}</th>" for c in t["cols"]) + "<th>Copy</th>"
    rows = []
    for r in t["rows"]:
        first_cls = "symbol" if t.get("symbol") else "keys"
        cells = f'<td class="{first_cls}">{esc(r[0])}</td>' + "".join(
            f"<td>{esc(c)}</td>" for c in r[1:])
        rows.append(f" <tr>{cells}<td><button class=\"copy-btn\">Copy</button></td></tr>")
    howto = f' <div class="howto">{t["howto"]}</div>\n' if t.get("howto") else ""
    return f""" <h2>{esc(t["title"])}</h2>
{howto} <input class="search" data-table="list{i}" placeholder="Search... (jaise copy, save)" aria-label="Search {esc(t["title"])}">
 <div class="table-wrap">
 <table>
 <thead><tr>{head}</tr></thead>
 <tbody id="list{i}">
{chr(10).join(rows)}
 </tbody>
 </table>
 </div>
"""


def page_html(p):
    url = SITE + p["file"]
    count = sum(len(t["rows"]) for t in p["tables"])
    tables = "\n".join(
        f'<section>\n{table_html(t, i)}</section>' for i, t in enumerate(p["tables"]))
    others = "\n".join(
        f'  <a class="card" href="{o["file"]}"><h3>{o["emoji"]} {o["nav"]}</h3></a>'
        for o in PAGES if o["file"] != p["file"])
    ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Shortcut Guru", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": p["nav"], "item": url},
        ],
    }
    plain_h1 = html.unescape(p["h1"].replace("<span>", "").replace("</span>", ""))
    return f"""<!DOCTYPE html>
<!-- Generated by tools/build_pages.py – edit the data there, not this file. -->
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["description"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Shortcut Guru">
<meta property="og:title" content="{esc(plain_h1)}">
<meta property="og:description" content="{esc(p["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}icons/icon-512.png">
<meta name="twitter:card" content="summary">
<link rel="manifest" href="/shortcut/manifest.json">
<meta name="theme-color" content="#e50914">
<link rel="icon" type="image/png" href="/shortcut/icons/icon-192.png">
<link rel="apple-touch-icon" href="/shortcut/icons/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Shortcut Guru">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>

<header>
 <div class="logo"><a href="./">SHORTCUT <span>GURU</span></a></div>
 <nav>
{nav_html(p["file"])}
 </nav>
</header>

<main>
<section class="page-hero">
 <p class="crumb"><a href="./">Home</a> › {p["nav"]}</p>
 <h1>{p["emoji"]} {p["h1"]}</h1>
 <p>{esc(p["intro"])}</p>
 <p>Is page par <b>{count}</b> shortcuts hain. Search box mein likh kar dhoondo aur <b>Copy</b> dabao.</p>
</section>

{tables}
<section class="cta">
 <h2>🎬 Video mein seekho</h2>
 <p>Har roz naye shortcut aur computer tricks ke Shorts – channel subscribe karo.</p>
 <a class="btn" href="{YOUTUBE}" target="_blank" rel="noopener noreferrer">▶️ SUBSCRIBE ON YOUTUBE</a>
</section>

<section>
 <h2>Aur Shortcuts Dekho</h2>
 <div class="grid">
{others}
 </div>
</section>
</main>

<footer>
 <div class="social">
  <a class="yt" href="{YOUTUBE}" target="_blank" rel="noopener noreferrer">▶️ YouTube</a>
  <a class="ig" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">📸 Instagram</a>
 </div>
 <p>© 2026 Shortcut Guru | Learn Smart, Work Fast</p>
</footer>

<script>
document.querySelectorAll("input.search").forEach(function(input){{
 var rows=document.querySelectorAll("#"+input.dataset.table+" tr");
 input.addEventListener("input",function(){{
  var v=this.value.toLowerCase();
  rows.forEach(function(r){{ r.hidden=!r.textContent.toLowerCase().includes(v); }});
 }});
}});
document.querySelectorAll(".copy-btn").forEach(function(b){{
 b.addEventListener("click",async function(){{
  var v=this.closest("tr").cells[0].textContent.trim();
  try{{ await navigator.clipboard.writeText(v); this.textContent="Copied!"; }}
  catch(e){{ this.textContent="Failed"; }}
  var btn=this; setTimeout(function(){{ btn.textContent="Copy"; }},1200);
 }});
}});
if("serviceWorker" in navigator){{
 window.addEventListener("load",function(){{
  navigator.serviceWorker.register("/shortcut/service-worker.js").catch(function(){{}});
 }});
}}
</script>
</body>
</html>
"""


def sitemap():
    urls = [(SITE, "1.0")] + [(SITE + p["file"], "0.9") for p in PAGES]
    pdfs = sorted(f for f in os.listdir(os.path.join(ROOT, "pdf")) if f.endswith(".pdf"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, prio in urls:
        out.append(f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod><priority>{prio}</priority></url>")
    for f in pdfs:
        out.append(f"  <url><loc>{SITE}pdf/{f}</loc></url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    for p in PAGES:
        with open(os.path.join(ROOT, p["file"]), "w", encoding="utf-8") as f:
            f.write(page_html(p))
        print("wrote", p["file"], sum(len(t["rows"]) for t in p["tables"]), "rows")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
