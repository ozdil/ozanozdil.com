import os
import re
import json
import html
from urllib.parse import urlparse
from html.parser import HTMLParser

FEED_PATH = "/home/ozdil/.gemini/antigravity/brain/6813f414-850d-4b36-a322-257511dbf362/scratch/blogger_feed.json"
OUTPUT_DIR = "src/content/blog"
REDIRECTS_FILE = "public/_redirects"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("public", exist_ok=True)

with open(FEED_PATH, "r", encoding="utf-8") as f:
    feed = json.load(f)

entries = feed["feed"]["entry"]
print(f"Loaded {len(entries)} entries from Blogger feed.")

class HTMLToMarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_script = False
        self.in_style = False
        self.in_pre = False
        self.in_code = False
        self.list_stack = []
        self.current_href = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        tag = tag.lower()

        if tag in ["script", "style"]:
            if tag == "script":
                self.in_script = True
            elif tag == "style":
                self.in_style = True
            return

        if self.in_script or self.in_style:
            return

        if tag == "pre":
            self.in_pre = True
            self.result.append("\n\n```code\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.result.append("`")
        elif tag in ["h1", "h2"]:
            self.result.append("\n\n## ")
        elif tag == "h3":
            self.result.append("\n\n### ")
        elif tag == "h4":
            self.result.append("\n\n#### ")
        elif tag in ["h5", "h6"]:
            self.result.append("\n\n##### ")
        elif tag == "p":
            self.result.append("\n\n")
        elif tag == "br":
            self.result.append("\n")
        elif tag == "hr":
            self.result.append("\n\n---\n\n")
        elif tag in ["strong", "b"]:
            self.result.append("**")
        elif tag in ["em", "i"]:
            self.result.append("*")
        elif tag == "blockquote":
            self.result.append("\n\n> ")
        elif tag == "ul":
            self.list_stack.append("ul")
            self.result.append("\n")
        elif tag == "ol":
            self.list_stack.append("ol")
            self.result.append("\n")
        elif tag == "li":
            indent = "  " * (len(self.list_stack) - 1) if self.list_stack else ""
            prefix = "1. " if self.list_stack and self.list_stack[-1] == "ol" else "- "
            self.result.append(f"\n{indent}{prefix}")
        elif tag == "a":
            self.current_href = attr_dict.get("href", "")
            self.result.append("[")
        elif tag == "img":
            src = attr_dict.get("src", "")
            alt = attr_dict.get("alt", "").strip() or "Görsel"
            src = re.sub(r"/s[0-9]+(-c)?/", "/s1600/", src)
            self.result.append(f"\n\n![{alt}]({src})\n\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "script":
            self.in_script = False
            return
        if tag == "style":
            self.in_style = False
            return
        if self.in_script or self.in_style:
            return

        if tag == "pre":
            self.in_pre = False
            self.result.append("\n```\n\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = False
            self.result.append("`")
        elif tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p"]:
            self.result.append("\n\n")
        elif tag in ["strong", "b"]:
            self.result.append("**")
        elif tag in ["em", "i"]:
            self.result.append("*")
        elif tag == "blockquote":
            self.result.append("\n\n")
        elif tag in ["ul", "ol"]:
            if self.list_stack:
                self.list_stack.pop()
            self.result.append("\n")
        elif tag == "a":
            href = self.current_href or ""
            self.result.append(f"]({href})")
            self.current_href = None

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        self.result.append(data)

    def get_markdown(self):
        raw = "".join(self.result)
        raw = html.unescape(raw)
        return raw

def format_markdown(raw_md, post_title):
    lines = raw_md.split("\n")
    cleaned_lines = []
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            cleaned_lines.append(line.strip())
            continue
        if in_code:
            cleaned_lines.append(line)
            continue
        
        # For regular text lines, trim extra trailing/leading indentation
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            cleaned_lines.append("- " + s[2:].strip())
        elif re.match(r'^[0-9]+\.\s+', s):
            m = re.match(r'^([0-9]+\.\s+)(.*)', s)
            cleaned_lines.append(m.group(1) + m.group(2).strip())
        elif s.startswith(">"):
            quote_body = s[1:].strip()
            if quote_body:
                cleaned_lines.append("> " + quote_body)
            else:
                cleaned_lines.append("")
        elif s.startswith("#"):
            cleaned_lines.append(s)
        else:
            cleaned_lines.append(s)

    # Join and collapse 3+ newlines to 2
    md = "\n".join(cleaned_lines)
    md = re.sub(r'\n{3,}', '\n\n', md)
    # Clean bold markers
    md = re.sub(r'\*\*\s+\*\*', '', md)
    md = re.sub(r'\*\*\s+(.*?)\s+\*\*', r'**\1**', md)
    md = md.strip()

    # Drop duplicated first title if it matches post_title
    lines = md.split("\n")
    if lines and lines[0].startswith("## "):
        h_text = lines[0].replace("## ", "").strip()
        if h_text.lower() in post_title.lower() or post_title.lower() in h_text.lower():
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines = lines[1:]
            md = "\n".join(lines).strip()

    # Detect code block languages
    def code_block_tagger(match):
        code = match.group(1)
        if any(w in code for w in ["sudo ", "pacman ", "systemctl", "yay -S", "curl ", "chmod ", "apt ", "dnf "]):
            return f"\n```bash\n{code.strip()}\n```\n"
        elif any(w in code for w in ["import ", "def ", "class ", "print(", "from "]):
            return f"\n```python\n{code.strip()}\n```\n"
        elif code.strip().startswith("{") and code.strip().endswith("}"):
            return f"\n```json\n{code.strip()}\n```\n"
        elif "<?xml" in code or "<html" in code or "<div" in code:
            return f"\n```html\n{code.strip()}\n```\n"
        return f"\n```text\n{code.strip()}\n```\n"

    md = re.sub(r'```code\n(.*?)```', code_block_tagger, md, flags=re.DOTALL)
    return md

def clean_html_to_markdown(raw_html, post_title):
    json_ld_desc = None
    json_ld_keywords = []

    json_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', raw_html, re.DOTALL)
    if json_match:
        try:
            jd = json.loads(json_match.group(1))
            if "@graph" in jd:
                for item in jd["@graph"]:
                    if "description" in item and not json_ld_desc:
                        json_ld_desc = item["description"]
                    if "keywords" in item and not json_ld_keywords:
                        json_ld_keywords = [k.strip() for k in item["keywords"].split(",") if k.strip()]
            elif "description" in jd:
                json_ld_desc = jd["description"]
        except Exception:
            pass

    parser = HTMLToMarkdownParser()
    parser.feed(raw_html)
    raw_md = parser.get_markdown()
    md = format_markdown(raw_md, post_title)

    # Clean description
    if not json_ld_desc:
        clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', md)
        clean_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_text)
        clean_text = re.sub(r'[#*`>-]', '', clean_text)
        clean_text = ' '.join(clean_text.split())
        sentences = [s.strip() for s in clean_text.split('.') if len(s.strip()) > 20]
        if sentences:
            desc = sentences[0]
            if len(desc) < 110 and len(sentences) > 1:
                desc += '. ' + sentences[1]
            if len(desc) > 160:
                desc = desc[:157] + '...'
            elif not desc.endswith('.'):
                desc += '.'
            json_ld_desc = desc
        else:
            json_ld_desc = post_title

    json_ld_desc = json_ld_desc.replace('"', "'").strip()
    return md, json_ld_desc, json_ld_keywords

redirect_rules = [
    "# Cloudflare Pages 301 Permanent Redirects for Blogger Legacy URLs",
    "/:year/:month/:slug.html /blog/:slug 301"
]

migrated_count = 0

for i, e in enumerate(entries):
    title = html.unescape(e['title']['$t'].strip())
    pub_date = e['published']['$t']
    updated_date = e.get('updated', {}).get('$t')
    
    alt_link = next((l['href'] for l in e.get('link', []) if l.get('rel') == 'alternate'), '')
    if not alt_link:
        continue

    parsed_url = urlparse(alt_link)
    legacy_path = parsed_url.path
    slug = legacy_path.split('/')[-1].replace('.html', '')

    raw_html = e.get('content', {}).get('$t', '')

    hero_image = ""
    thumb = e.get('media$thumbnail', {}).get('url')
    if thumb:
        hero_image = re.sub(r"/s[0-9]+(-c)?/", "/s1600/", thumb)
    elif '<img' in raw_html:
        m_img = re.search(r'src=["\'](https?://[^"\']+)["\']', raw_html)
        if m_img:
            hero_image = re.sub(r"/s[0-9]+(-c)?/", "/s1600/", m_img.group(1))

    categories = [c.get('term', '').strip() for c in e.get('category', []) if c.get('term')]
    md_content, desc, extra_keywords = clean_html_to_markdown(raw_html, title)

    all_tags = []
    for t in categories + extra_keywords:
        t_clean = t.lower().strip()
        if t_clean and t_clean not in all_tags and len(t_clean) < 30:
            all_tags.append(t_clean)
    if not all_tags:
        all_tags = ["teknoloji", "sistem", "guvenlik"]

    safe_title = title.replace('"', '\\"')
    safe_desc = desc.replace('"', '\\"')

    fm = [
        "---",
        f'title: "{safe_title}"',
        f'description: "{safe_desc}"',
        f'pubDate: "{pub_date}"'
    ]
    if updated_date and updated_date != pub_date:
        fm.append(f'updatedDate: "{updated_date}"')
    if hero_image:
        fm.append(f'heroImage: "{hero_image}"')
    
    tags_str = ", ".join([f'"{t}"' for t in all_tags[:6]])
    fm.append(f'tags: [{tags_str}]')
    fm.append('draft: false')
    fm.append(f'legacyUrl: "{legacy_path}"')
    fm.append("---")
    fm.append("")
    fm.append(md_content)
    fm.append("")

    target_file = os.path.join(OUTPUT_DIR, f"{slug}.md")
    with open(target_file, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(fm))

    redirect_rules.append(f"{legacy_path} /blog/{slug} 301")
    migrated_count += 1
    print(f"[{migrated_count:2d}/26] Migrated: {slug} ({pub_date[:10]})")

with open(REDIRECTS_FILE, "w", encoding="utf-8") as rf:
    rf.write("\n".join(redirect_rules) + "\n")

print(f"\nMigration successfully completed: {migrated_count} articles written to {OUTPUT_DIR}/")
print(f"Cloudflare Pages redirects written to {REDIRECTS_FILE} ({len(redirect_rules)} rules)")
