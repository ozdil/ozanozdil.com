interface Env {
  ASSETS: {
    fetch: (request: Request | string) => Promise<Response>;
  };
}

export const onRequest: PagesFunction<Env> = async (context) => {
  const request = context.request;
  const accept = request.headers.get('Accept') || '';
  const url = new URL(request.url);

  // 1. Content Negotiation: Accept: text/markdown
  if (
    accept.includes('text/markdown') &&
    !url.pathname.endsWith('.txt') &&
    !url.pathname.endsWith('.json') &&
    !url.pathname.endsWith('.xml') &&
    !url.pathname.endsWith('.png') &&
    !url.pathname.endsWith('.jpg') &&
    !url.pathname.endsWith('.webp')
  ) {
    // If requesting homepage or generic HTML page
    if (url.pathname === '/' || url.pathname === '' || url.pathname === '/index.html') {
      const llmsUrl = new URL('/llms.txt', request.url);
      const res = await context.env.ASSETS.fetch(llmsUrl.toString());
      if (res.ok) {
        const text = await res.text();
        const tokens = Math.ceil(text.length / 4);
        return new Response(text, {
          status: 200,
          headers: {
            'Content-Type': 'text/markdown; charset=utf-8',
            'x-markdown-tokens': tokens.toString(),
            'Vary': 'Accept',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }
    }
  }

  // 2. Fetch origin asset
  const response = await context.next();

  // 3. Ensure Link headers on homepage
  if (url.pathname === '/' || url.pathname === '' || url.pathname === '/index.html') {
    const newHeaders = new Headers(response.headers);
    newHeaders.set(
      'Link',
      '</.well-known/api-catalog>; rel="api-catalog", </.well-known/ai-catalog.json>; rel="service-desc", </llms.txt>; rel="describedby"'
    );
    newHeaders.set('Access-Control-Allow-Origin', '*');
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  }

  return response;
};
