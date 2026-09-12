import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const siteUrl = context.site ? context.site.toString().replace(/\/$/, '') : 'https://ozanozdil.com';

  const body = JSON.stringify({
    linkset: [
      {
        anchor: `${siteUrl}/api`,
        "service-doc": [
          {
            href: `${siteUrl}/llms.txt`,
            type: "text/plain"
          }
        ],
        "service-desc": [
          {
            href: `${siteUrl}/.well-known/ai-catalog.json`,
            type: "application/json"
          }
        ]
      }
    ]
  }, null, 2);

  return new Response(body, {
    status: 200,
    headers: {
      'Content-Type': 'application/linkset+json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}
