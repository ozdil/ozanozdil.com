interface Env {
  ASSETS: {
    fetch: (request: Request | string) => Promise<Response>;
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const accept = request.headers.get('Accept') || '';

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
      if (url.pathname === '/' || url.pathname === '' || url.pathname === '/index.html') {
        const llmsUrl = new URL('/llms.txt', request.url);
        const res = await env.ASSETS.fetch(new Request(llmsUrl.toString()));
        if (res.ok) {
          const text = await res.text();
          const tokens = Math.ceil(text.length / 4);
          return new Response(text, {
            status: 200,
            headers: {
              'Content-Type': 'text/markdown; charset=utf-8',
              'x-markdown-tokens': tokens.toString(),
              'Vary': 'Accept',
              'Access-Control-Allow-Origin': '*',
              'Cache-Control': 'public, max-age=60'
            }
          });
        }
      }
    }

    const response = await env.ASSETS.fetch(request);

    // Ensure Link headers on homepage
    if (url.pathname === '/' || url.pathname === '' || url.pathname === '/index.html') {
      const newHeaders = new Headers(response.headers);
      newHeaders.set(
        'Link',
        '</.well-known/api-catalog>; rel="api-catalog", </.well-known/ai-catalog.json>; rel="service-desc", </llms.txt>; rel="describedby"'
      );
      newHeaders.set('Access-Control-Allow-Origin', '*');
      newHeaders.set('Vary', 'Accept');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders
      });
    }

    return response;
  }
};
