interface KVNamespaceLike {
  get: (key: string) => Promise<string | null>;
  put: (key: string, value: string) => Promise<void>;
  list: (options?: { prefix?: string; limit?: number }) => Promise<{ keys: Array<{ name: string }> }>;
}

interface Env {
  ASSETS: {
    fetch: (request: Request | string) => Promise<Response>;
  };
  AI?: {
    run: (model: string, options: any) => Promise<any>;
  };
  BLOG_VIEWS?: KVNamespaceLike;
}

function getBaseViews(slug: string): number {
  let hash = 0;
  for (let i = 0; i < slug.length; i++) {
    hash = ((hash << 5) - hash) + slug.charCodeAt(i);
    hash |= 0;
  }
  return 220 + (Math.abs(hash) % 480);
}

const OZAN_SYSTEM_PROMPT = `Sen Ozan Özdil'in (ozanozdil.com) web sitesindeki resmi Yapay Zeka Dijital İkizi ve Asistanısın (Ozan AI).
Görevin, ziyaretçilere Ozan Özdil'in projelerini, teknik felsefesini, blog yazılarını, açık kaynak çalışmalarını ve donanım deneyimlerini samimi, profesyonel, teknik olarak tutarlı ve yardımcı bir dille anlatmaktır.

TEMEL İLKELER:
1. Ziyaretçinin konuştuğu dilde yanıt ver (genellikle Türkçe, soru İngilizce ise İngilizce).
2. Yanıtların net, akıcı, bilgilendirici ve samimi olsun. Çok uzun destanlar yazmak yerine vurucu ve doğru bilgiler ver.
3. Bahsettiğin konularda uygunsa web sitesindeki sayfalara veya GitHub linklerine markdown bağlantısı ver.
4. Ozan Özdil'in uzmanlık alanları dışındaki konularda konuyu Ozan'ın çalışmalarına veya açık kaynak felsefesine bağla; uydurma yapma.
5. Doğal, duru ve akıcı bir Türkçe kullan; teknik terimleri doğru aktar (örneğin 'developer-centric' için 'geliştirici odaklı' de).

OZAN ÖZDİL HAKKINDA BİLGİ BANKASI:
- Kimdir: YZ Kodcusu (AI Coder), açık kaynak sistem araştırmacısı, Linux/Arch/CachyOS/Omarchy meraklısı ve geliştiricisi, Steam Deck tutkunu, bağımsız fotoğrafçı.
- Temel Uzmanlıklar: Arch Linux, CachyOS, Omarchy, Wayland (Hyprland), Quickshell (Qt/QML), Rust, modern web ve YZ ajanları, Steam Deck oyun & donanım optimizasyonu, siber güvenlik, dijital egemenlik, Fujifilm GFX orta format fotoğrafçılık.
- Önemli Bağlantılar:
  * Ana Sayfa: https://ozanozdil.com
  * Blog (45+ Teknik Makale): https://ozanozdil.com/blog
  * Açık Kaynak Projeler: https://ozanozdil.com/projeler
  * Fotoğraf Galerisi: https://ozanozdil.com/galeri
  * Biyografi & İletişim: https://ozanozdil.com/hakkimda
  * GitHub: https://github.com/ozdil
  * Steam: https://steamcommunity.com/id/ozanozdil
  * nSosyal: https://nsosyal.com/ozanozdil

ÖNE ÇIKAN AÇIK KAYNAK PROJELER:
1. omarchy-omanotes: Rust ve QML tabanlı, Zero-Knowledge AES-256-GCM uçtan uca şifreli (E2EE), Google Drive / Git bulut senkronizasyonlu Google Keep tarzı not uygulaması. (https://github.com/ozdil/omarchy-omanotes)
2. omarchy-shell: Quickshell tabanlı, Qt/QML çekirdekli modern Wayland masaüstü kabuğu.
3. quickshell-oled-themes / omarchy-turkiye-theme: 4K OLED optimize tema motoru, Catppuccin ve Türk bayrağı paletleri.
4. quickshell-game-hud: Linux oyuncuları için tam ekran Game Mode ve OSD performans paneli.
5. omarchy: Arch Linux tabanlı, optimize edilmiş dotfiles ve sistem yapılandırması.
6. omarchy-cyber-sentinel: Ağ trafiği izleme ve anormallik tespit aracı.
7. omarchy-badusb-shield: BadUSB donanım saldırılarına karşı koruma ve USB aygıt yetkilendirme kalkanı.
8. omarchy-cve-radar: Linux sistem paketleri için CVE güvenlik açığı denetleyici.
9. omarchy-omarank: Linux donanım ve çekirdek performans kıyaslama aracı.
10. omarchy-omasend & omasend-android: AirDrop benzeri yerel P2P dosya aktarımı ve pano eşitleme aracı (Linux için Rust/QML, Android için Kotlin/Compose).
11. omarchy-auth-watch: Yetkisiz oturum açma ve SSH denemelerini izleme güvenlik aracı.
12. omarchy-ghost-mac: Kablosuz ağ MAC adreslerini dinamik olarak anonimleştiren gizlilik aracı.
13. omarchy-dns-leak-guard: DNS sızıntılarını denetleyen ve DoH/DoT şifreli DNS tünellemesini doğrulayan araç.
14. omarchy-tripwire-vault: Dosya sistemi yetkisiz erişim tespit ve honeypot aracı.

ÖNE ÇIKAN BLOG KONULARI:
- Steam Deck & Linux Oyunculuğu: Steam Deck OLED optimizasyonları, Proton GE, Gamescope, TDP yönetimi, pil tasarrufu.
- Linux & Sistem: CachyOS (x86-64-v3/v4 çekirdek optimizasyonu), Arch Linux, Omarchy yapılandırması, Wayland/Hyprland, Btrfs anlık görüntüleri, ZRAM/zswap.
- Güvenlik & YZ: Siber güvenlik eklentileri, LLM ajanları, dijital egemenlik, yerel yapay zeka modelleri.
- Fotoğrafçılık: Fujifilm GFX 50R ve GFX 100 ile Karadeniz, Ağlı Kalesi ve UNESCO ahşap camileri serileri.`;

function getFallbackAnswer(query: string): string {
  const q = query.toLowerCase();
  if (q.includes('omanote') || q.includes('not')) {
    return "Ozan'ın geliştirdiği **omarchy-omanotes**, Rust ve QML ile yazılmış, Google Keep benzeri modern bir not defteridir. En önemli özelliği Zero-Knowledge AES-256-GCM uçtan uca şifreleme (E2EE) ve Google Drive/Git bulut senkronizasyonu sunmasıdır. Detaylar ve kaynak kod için [GitHub: omarchy-omanotes](https://github.com/ozdil/omarchy-omanotes) deposuna göz atabilirsiniz!";
  }
  if (q.includes('steam') || q.includes('deck') || q.includes('oyun') || q.includes('fps')) {
    return "Ozan, Steam Deck ve Linux oyunculuğu üzerine kapsamlı donanım ve yazılım optimizasyonları yapmaktadır. Proton GE ayarları, Gamescope yapılandırmaları, TDP yönetimi ve batarya optimizasyonu hakkında detaylı rehberler hazırlamıştır. [Yazılar](https://ozanozdil.com/blog) sayfasından Steam Deck incelemelerine ve [Steam Profiline](https://steamcommunity.com/id/ozanozdil) ulaşabilirsiniz.";
  }
  if (q.includes('proje') || q.includes('eklenti') || q.includes('plugin') || q.includes('github') || q.includes('kod')) {
    return "Ozan Özdil'in geliştirdiği öne çıkan açık kaynak projeler arasında **omarchy-omanotes** (şifreli not defteri), **omarchy-omasend** (yerel P2P dosya paylaşımı), **omarchy-shell** (Quickshell tabanlı Wayland kabuğu) ve 9 farklı siber güvenlik aracı (Cyber Sentinel, BadUSB Shield, CVE Radar vb.) bulunmaktadır. Tüm projelere [Projeler](https://ozanozdil.com/projeler) sayfasından veya [GitHub: @ozdil](https://github.com/ozdil) üzerinden ulaşabilirsiniz.";
  }
  if (q.includes('kim') || q.includes('hakkında') || q.includes('ozan kim')) {
    return "Ozan Özdil; YZ Kodcusu (AI Coder), açık kaynak sistem araştırmacısı, Linux/Arch/CachyOS/Omarchy geliştiricisi, Steam Deck meraklısı ve Fujifilm GFX orta format fotoğrafçısıdır. Detaylı biyografisi ve vizyonu için [Hakkımda](https://ozanozdil.com/hakkimda) sayfasını inceleyebilirsiniz.";
  }
  if (q.includes('fotoğraf') || q.includes('galeri') || q.includes('kamera') || q.includes('gfx')) {
    return "Ozan, Fujifilm GFX 50R ve GFX 100 orta format kameralarla UNESCO tescilli tarihi ahşap camileri, Kastamonu Ağlı Kalesi'ni ve Karadeniz yaylalarını belgelemektedir. Fotoğraf çalışmalarını [Fotoğraf Galerisi](https://ozanozdil.com/galeri) sayfasında yüksek çözünürlükle keşfedebilirsiniz.";
  }
  if (q.includes('iletişim') || q.includes('ulaş') || q.includes('sosyal') || q.includes('mail')) {
    return "Ozan ile [GitHub (@ozdil)](https://github.com/ozdil), [nSosyal (@ozanozdil)](https://nsosyal.com/ozanozdil) veya [Steam](https://steamcommunity.com/id/ozanozdil) üzerinden iletişim kurabilirsiniz. Daha fazla bilgi için [Hakkımda](https://ozanozdil.com/hakkimda) sayfasını ziyaret edebilirsiniz.";
  }
  return "Merhabalar! Ben Ozan Özdil'in Yapay Zeka Asistanıyım. Ozan'ın geliştirdiği açık kaynak projeler (OmaNotes, OmaSend, güvenlik araçları), Linux/CachyOS sistem yapılandırmaları, Steam Deck optimizasyonları veya blog makaleleri hakkında dilediğinizi sorabilirsiniz. Daha fazla keşif için [Projeler](https://ozanozdil.com/projeler) ve [Yazılar](https://ozanozdil.com/blog) sayfalarımıza da göz atabilirsiniz.";
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const accept = request.headers.get('Accept') || '';

    // Handle CORS preflight for API routes
    if (request.method === 'OPTIONS' && url.pathname.startsWith('/api/')) {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    // Handle Article Views API: /api/views
    if (url.pathname === '/api/views') {
      const corsHeaders = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-store, max-age=0',
      };

      if (!env.BLOG_VIEWS) {
        return new Response(JSON.stringify({ error: 'KV not configured', views: 0 }), {
          status: 200,
          headers: corsHeaders,
        });
      }

      if (request.method === 'GET') {
        const slug = (url.searchParams.get('slug') || '').trim().toLowerCase();
        if (!slug) {
          return new Response(JSON.stringify({ error: 'Slug required', views: 0 }), {
            status: 400,
            headers: corsHeaders,
          });
        }
        const safeSlug = slug.replace(/[^a-z0-9\-_]/g, '').slice(0, 100);
        const stored = await env.BLOG_VIEWS.get(`views:${safeSlug}`);
        const views = stored !== null ? Number(stored) : getBaseViews(safeSlug);
        return new Response(JSON.stringify({ slug: safeSlug, views }), {
          status: 200,
          headers: corsHeaders,
        });
      }

      if (request.method === 'POST') {
        try {
          const body = (await request.json()) as { slug?: string };
          const slug = (body.slug || '').trim().toLowerCase();
          if (!slug) {
            return new Response(JSON.stringify({ error: 'Slug required', views: 0 }), {
              status: 400,
              headers: corsHeaders,
            });
          }
          const safeSlug = slug.replace(/[^a-z0-9\-_]/g, '').slice(0, 100);

          const userAgent = (request.headers.get('User-Agent') || '').toLowerCase();
          const isBot = /bot|crawl|spider|google|bing|yandex|baidu|slurp|curl|wget|python|facebook|whatsapp|telegram|cf-worker/i.test(userAgent);

          const stored = await env.BLOG_VIEWS.get(`views:${safeSlug}`);
          let views: number;
          if (stored !== null) {
            views = Number(stored);
            if (!isBot) {
              views += 1;
              await env.BLOG_VIEWS.put(`views:${safeSlug}`, String(views));
            }
          } else {
            views = getBaseViews(safeSlug);
            if (!isBot) {
              views += 1;
            }
            await env.BLOG_VIEWS.put(`views:${safeSlug}`, String(views));
          }

          return new Response(JSON.stringify({ slug: safeSlug, views }), {
            status: 200,
            headers: corsHeaders,
          });
        } catch (e: any) {
          return new Response(JSON.stringify({ error: e.message, views: 0 }), {
            status: 500,
            headers: corsHeaders,
          });
        }
      }

      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: corsHeaders,
      });
    }

    // Top Popular Articles API: /api/views/top
    if (url.pathname === '/api/views/top') {
      const corsHeaders = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=60',
      };

      if (!env.BLOG_VIEWS) {
        return new Response(JSON.stringify({ top: [] }), { status: 200, headers: corsHeaders });
      }

      try {
        const list = await env.BLOG_VIEWS.list({ prefix: 'views:' });
        const items = await Promise.all(
          list.keys.slice(0, 20).map(async (k) => {
            const val = await env.BLOG_VIEWS!.get(k.name);
            return {
              slug: k.name.replace(/^views:/, ''),
              views: Number(val || 0),
            };
          })
        );
        items.sort((a, b) => b.views - a.views);
        return new Response(JSON.stringify({ top: items.slice(0, 10) }), {
          status: 200,
          headers: corsHeaders,
        });
      } catch (e: any) {
        return new Response(JSON.stringify({ top: [], error: e.message }), {
          status: 500,
          headers: corsHeaders,
        });
      }
    }

    // Handle AI Chat Endpoint: POST /api/chat
    if (url.pathname === '/api/chat') {
      if (request.method !== 'POST') {
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
          status: 405,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      try {
        const body = (await request.json()) as {
          message?: string;
          history?: Array<{ role: 'user' | 'assistant'; content: string }>;
        };

        const userMessage = (body.message || '').trim();
        if (!userMessage) {
          return new Response(JSON.stringify({ error: 'Mesaj boş olamaz' }), {
            status: 400,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
            },
          });
        }

        let answer = '';
        let debugInfo: any = null;

        // Check if Cloudflare Workers AI is available
        if (env.AI && typeof env.AI.run === 'function') {
          try {
            const rawHistory = Array.isArray(body.history) ? body.history.slice(-6) : [];
            const sanitizedHistory = rawHistory.map((m) => ({
              role: m.role === 'assistant' ? 'assistant' : 'user',
              content: String(m.content || '').slice(0, 1000),
            }));

            const messages = [
              { role: 'system', content: OZAN_SYSTEM_PROMPT },
              ...sanitizedHistory,
              { role: 'user', content: userMessage.slice(0, 1000) },
            ];

            let aiResponse: any = null;
            try {
              aiResponse = await env.AI.run('@cf/meta/llama-3.1-8b-instruct-fp8', {
                messages,
                max_tokens: 600,
                temperature: 0.6,
              });
            } catch (firstErr) {
              console.warn('Llama 3.1 8B FP8 failed, trying Llama 3.2 3B:', firstErr);
              aiResponse = await env.AI.run('@cf/meta/llama-3.2-3b-instruct', {
                messages,
                max_tokens: 600,
                temperature: 0.6,
              });
            }

            if (aiResponse && typeof aiResponse === 'object') {
              if (typeof aiResponse.response === 'string' && aiResponse.response.trim()) {
                answer = aiResponse.response.trim();
              } else if (aiResponse.result && typeof aiResponse.result.response === 'string') {
                answer = aiResponse.result.response.trim();
              }
            }
          } catch (aiErr: any) {
            console.error('Workers AI execution error:', aiErr);
          }
        }

        // Fallback to grounded intelligent rule responder if AI is unavailable or didn't return text
        if (!answer) {
          answer = getFallbackAnswer(userMessage);
        }

        return new Response(JSON.stringify({ answer }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-store',
          },
        });
      } catch (err: any) {
        return new Response(
          JSON.stringify({
            answer: getFallbackAnswer(''),
            warning: 'İstek işlenirken bir sorun oluştu.',
          }),
          {
            status: 200,
            headers: {
              'Content-Type': 'application/json; charset=utf-8',
              'Access-Control-Allow-Origin': '*',
            },
          }
        );
      }
    }

    // Handle Content Negotiation: Accept: text/markdown
    if (
      accept.includes('text/markdown') &&
      !url.pathname.endsWith('.txt') &&
      !url.pathname.endsWith('.json') &&
      !url.pathname.endsWith('.xml') &&
      !url.pathname.endsWith('.png') &&
      !url.pathname.endsWith('.jpg') &&
      !url.pathname.endsWith('.webp')
    ) {
      // 1. Homepage / root / blog list -> llms.txt
      if (
        url.pathname === '/' ||
        url.pathname === '' ||
        url.pathname === '/index.html' ||
        url.pathname === '/blog' ||
        url.pathname === '/blog/' ||
        url.pathname === '/projeler' ||
        url.pathname === '/projeler/' ||
        url.pathname === '/hakkimda' ||
        url.pathname === '/hakkimda/'
      ) {
        const llmsUrl = new URL('/llms.txt', request.url);
        const res = await env.ASSETS.fetch(new Request(llmsUrl.toString(), { method: 'GET' }));
        if (res.ok) {
          const text = await res.text();
          const tokens = Math.ceil(text.length / 4);
          return new Response(request.method === 'HEAD' ? null : text, {
            status: 200,
            headers: {
              'Content-Type': 'text/markdown; charset=utf-8',
              'x-markdown-tokens': tokens.toString(),
              'Vary': 'Accept',
              'Access-Control-Allow-Origin': '*',
              'Cache-Control': 'public, max-age=300',
            },
          });
        }
      }

      // 2. Individual Blog Posts -> Extract raw markdown from embedded script
      if (url.pathname.startsWith('/blog/') && url.pathname !== '/blog/' && url.pathname !== '/blog') {
        const pageRes = await env.ASSETS.fetch(new Request(request.url, { method: 'GET' }));
        if (pageRes.ok) {
          const html = await pageRes.text();
          const match = html.match(/<script type="text\/plain" id="qs-raw-markdown"[^>]*>([\s\S]*?)<\/script>/);
          if (match) {
            try {
              const markdown = JSON.parse(match[1]);
              const tokens = Math.ceil(markdown.length / 4);
              return new Response(request.method === 'HEAD' ? null : markdown, {
                status: 200,
                headers: {
                  'Content-Type': 'text/markdown; charset=utf-8',
                  'x-markdown-tokens': tokens.toString(),
                  'Vary': 'Accept',
                  'Access-Control-Allow-Origin': '*',
                  'Cache-Control': 'public, max-age=300',
                },
              });
            } catch {
              // fallback to normal HTML if parsing fails
            }
          }
        }
      }
    }

    const response = await env.ASSETS.fetch(request);

    // LLM Context Files: add tokens and CORS
    if (url.pathname === '/llms.txt' || url.pathname === '/llms-full.txt') {
      const text = await response.text();
      const tokens = Math.ceil(text.length / 4);
      const newHeaders = new Headers(response.headers);
      newHeaders.set('Content-Type', 'text/plain; charset=utf-8');
      newHeaders.set('x-markdown-tokens', tokens.toString());
      newHeaders.set('Access-Control-Allow-Origin', '*');
      newHeaders.set('Vary', 'Accept');
      newHeaders.set('Cache-Control', 'public, max-age=3600');
      return new Response(text, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    // Web Bot Auth RFC 9421 Directory
    if (url.pathname === '/.well-known/http-message-signatures-directory') {
      const newHeaders = new Headers(response.headers);
      newHeaders.set('Content-Type', 'application/http-message-signatures-directory+json; charset=utf-8');
      newHeaders.set('Access-Control-Allow-Origin', '*');
      newHeaders.set('Cache-Control', 'public, max-age=3600');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    // OAuth Protected Resource RFC 9704 Metadata
    if (url.pathname === '/.well-known/oauth-protected-resource') {
      const origin = url.origin;
      return new Response(
        JSON.stringify(
          {
            resource: `${origin}/`,
            resource_name: 'Ozan Özdil Web and Agent API',
            resource_documentation: `${origin}/llms.txt`,
            authorization_servers: [origin],
            scopes_supported: ['read:articles', 'read:projects', 'public'],
            bearer_methods_supported: ['header'],
          },
          null,
          2
        ),
        {
          status: 200,
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'public, max-age=3600',
          },
        }
      );
    }

    // All HTML responses: attach Agent Discovery Link headers & security headers
    if (response.headers.get('content-type')?.includes('text/html')) {
      const newHeaders = new Headers(response.headers);
      newHeaders.set('Cache-Control', 'public, max-age=0, must-revalidate, stale-while-revalidate=86400');
      newHeaders.set(
        'Link',
        '</.well-known/api-catalog>; rel="api-catalog", </.well-known/ai-catalog.json>; rel="service-desc", </llms.txt>; rel="describedby", </.well-known/http-message-signatures-directory>; rel="http-message-signatures-directory", </auth.md>; rel="author-authorization"'
      );
      newHeaders.set('X-Content-Type-Options', 'nosniff');
      newHeaders.set('X-Frame-Options', 'SAMEORIGIN');
      newHeaders.set('Referrer-Policy', 'strict-origin-when-cross-origin');
      newHeaders.set('Access-Control-Allow-Origin', '*');
      newHeaders.set('Vary', 'Accept');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    // Static assets: images, fonts, hashed scripts/styles -> 1-year immutable cache
    if (
      url.pathname.startsWith('/_astro/') ||
      url.pathname.startsWith('/fonts/') ||
      url.pathname.startsWith('/images/') ||
      url.pathname.startsWith('/gallery/') ||
      url.pathname.endsWith('.woff2') ||
      url.pathname.endsWith('.webp') ||
      url.pathname.endsWith('.png') ||
      url.pathname.endsWith('.jpg') ||
      url.pathname.endsWith('.jpeg') ||
      url.pathname.endsWith('.svg') ||
      url.pathname.endsWith('.ico') ||
      url.pathname.endsWith('.css') ||
      url.pathname.endsWith('.js')
    ) {
      const newHeaders = new Headers(response.headers);
      newHeaders.set('Cache-Control', 'public, max-age=31536000, immutable');
      newHeaders.set('Access-Control-Allow-Origin', '*');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    }

    return response;
  },
};
