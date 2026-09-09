import json

DATA_FILE = "src/data/gallery.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

location_meta = {
    "agli-kalesi": {
        "title": "Ağlı Kalesi",
        "location": "Ağlı, Kastamonu",
        "locationFull": "Ağlı Kalesi, Ağlı / Kastamonu",
        "year": "2025",
        "dateFormatted": "Eylül 2025",
        "equipment": "Fujifilm GFX 50R • GF20-35mmF4 R WR",
        "description": "Ağlı Kalesi – Kastamonu Vadilerine Hükmeden Zirve Savunması\n\nAğlı ilçe merkezinde sarp bir kayalığın üzerine kurulu olan Ağlı Kalesi, Ortaçağ Anadolu savunma mimarisinin en etkileyici gözetleme noktalarından biridir. Bugün antik sur duvarlarının kalıntıları ayakta olsa da, kale Kastamonu'nun vadilerine, ormanlarına ve dağ silsilelerine hakim eşsiz bir panoramik görüş sunar.\n\nBizans ve erken dönem Türk beylikleri devirlerine uzanan kale, bölgedeki kritik geçiş yollarını denetim altında tutan stratejik bir karakol olarak hizmet vermiştir. Gece gökyüzü altında 60 saniyelik uzun pozlamalarla belgelenen bu seride, kadim taş duvarlar Samanyolu ve yıldız ışığıyla buluşmaktadır."
    },
    "seyh-saban-i-veli": {
        "title": "Şeyh Şaban-ı Veli Külliyesi",
        "location": "Hisarardı, Kastamonu Merkez",
        "locationFull": "Şeyh Şaban-ı Veli Külliyesi, Kastamonu",
        "year": "2020",
        "dateFormatted": "Kasım 2020",
        "equipment": "Fujifilm GFX 50R • GF50mmF3.5 R LM WR",
        "description": "Şeyh Şaban-ı Veli Külliyesi – Kastamonu'nun Manevi Sığınağı\n\nKastamonu'nun Hisarardı mahallesinde yer alan külliye, Halvetiyye-Şabaniyye kolunun kurucusu büyük veli Şeyh Şaban-ı Veli'ye ithaf edilmiş köklü bir ilim ve irfan merkezidir. 16. yüzyılda inşa edilen ve zamanla genişletilen külliye; cami, türbe, dergah konağı, şadırvan ve kütüphane yapılarından oluşur.\n\nSufi geleneğinin dinginlik ve tevazu felsefesini yansıtan taş işçiliği, ahşap bindirme saçaklar ve avlu kemerleri, Anadolu'nun asırlık zarafetini taşır. Bu seride külliyenin taş revakları, ahşap minber detayları ve dingin avlu mimarisi orta format detaycılığıyla kayda alınmıştır."
    },
    "nasrullah-meydani": {
        "title": "Nasrullah Meydanı ve Köprüsü",
        "location": "Kastamonu Kent Merkezi",
        "locationFull": "Nasrullah Meydanı, Kastamonu",
        "year": "2020",
        "dateFormatted": "Ekim 2020",
        "equipment": "Fujifilm GFX 50R • GF50mmF3.5 R LM WR",
        "description": "Nasrullah Meydanı – Kastamonu'nun Tarihi Kalbi\n\nNasrullah Meydanı, asırlardır Kastamonu'nun ticari, kültürel ve toplumsal yaşamının merkezinde yer alır. 1506 yılında Kadı Nasrullah tarafından yaptırılan cami ve külliye, Milli Mücadele yıllarında Mehmet Akif Ersoy'un Sebilürreşad vaazlarını verdiği tarihi bir hafıza mekanıdır.\n\nSekizgen mermer havuzlu anıtsal şadırvanı, tarihi köprüsü ve kesme taş revaklarıyla Anadolu şehir meydanı kimliğinin en özgün temsilcilerinden biridir. Fotoğraflar meydanın tarihi dokusunu, ışık-gölge oyunlarını ve gündelik hayatın ritmini belgeliyor."
    },
    "mahmutbey-camii": {
        "title": "Mahmutbey Camii (Kasaba Köyü)",
        "location": "Kasaba Köyü, Kastamonu (UNESCO)",
        "locationFull": "Kasaba Köyü Mahmutbey Camii, Kastamonu",
        "year": "2020",
        "dateFormatted": "Ekim 2020",
        "equipment": "Fujifilm GFX 100 (102MP) • GF23mmF4 R LM WR",
        "description": "Mahmutbey Camii – Çivisiz Ahşap Mimarinin Zirvesi (UNESCO Dünya Mirası)\n\nKastamonu merkeze bağlı Kasaba Köyü'nde 1366 yılında Candaroğulları Hükümdarı Emir Mahmut Bey tarafından yaptırılan cami, Anadolu Türk ahşap sanatının günümüze ulaşan en kusursuz örneğidir. Yapının en büyük özelliği, taşıyıcı sisteminde tek bir metal çivi dahi kullanılmadan kündekari ve geçme tekniğiyle inşa edilmiş olmasıdır.\n\nİç mekandaki ahşap sütunlar, konsollar, tavan kirişleri ve mahfil; kök boyası ile yapılmış benzersiz Selçuklu ve Beylikler dönemi geometrik/bitkisel motiflerle bezenmiştir. 102 Megapiksel Fujifilm GFX 100 ile çekilen bu kareler, yüzyıllardır solmayan kök boyası nakışları ve mikro ahşap dokularını ölümsüzleştirmektedir."
    }
}

enriched_albums = []
years_set = set()

for album in data["albums"]:
    slug = album["slug"]
    meta = location_meta.get(slug, {})
    
    album["title"] = meta.get("title", album["title"])
    album["location"] = meta.get("location", "Kastamonu")
    album["locationFull"] = meta.get("locationFull", "Kastamonu, Türkiye")
    album["year"] = meta.get("year", "2020")
    album["dateFormatted"] = meta.get("dateFormatted", album.get("shootDate", ""))
    album["equipment"] = meta.get("equipment", "Fujifilm GFX")
    album["description"] = meta.get("description", album["description"])
    
    years_set.add(album["year"])
    
    for idx, photo in enumerate(album["photos"]):
        photo["title"] = f"{album['title']} • Kare {idx + 1:02d}"
            
    enriched_albums.append(album)

enriched_albums.sort(key=lambda a: (int(a.get("year", 0)), a.get("dateCreated", 0)), reverse=True)
years_list = sorted(list(years_set), reverse=True)

data["albums"] = enriched_albums
data["years"] = years_list
data["totalAlbums"] = len(enriched_albums)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {len(enriched_albums)} albums across years: {years_list}")
for a in enriched_albums:
    print(f" - [{a['year']}] {a['title']} | Konum: {a['location']} | Fotoğraflar: {a['photoCount']}")
