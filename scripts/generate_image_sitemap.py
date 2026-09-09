import json

DATA_FILE = "src/data/gallery.json"
SITEMAP_FILE = "public/sitemap-images.xml"
SITE_URL = "https://ozanozdil.com"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    '  <url>',
    f'    <loc>{SITE_URL}/galeri</loc>',
    '    <changefreq>monthly</changefreq>',
    '    <priority>0.9</priority>'
]

for album in data["albums"]:
    location_name = album["locationFull"]
    for photo in album["photos"]:
        img_url = f"{SITE_URL}{photo['src']}"
        title = photo["title"]
        caption = photo["caption"]
        
        xml_lines.append('    <image:image>')
        xml_lines.append(f'      <image:loc>{img_url}</image:loc>')
        xml_lines.append(f'      <image:title><![CDATA[{title} - {location_name}]]></image:title>')
        xml_lines.append(f'      <image:caption><![CDATA[{caption} | Fotoğraf: Ozan Özdil]]></image:caption>')
        xml_lines.append(f'      <image:geo_location><![CDATA[{location_name}]]></image:geo_location>')
        xml_lines.append('    </image:image>')

xml_lines.append('  </url>')
xml_lines.append('</urlset>')

with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines) + "\n")

print(f"Generated {SITEMAP_FILE} with {data['totalPhotos']} Google Images entries.")
