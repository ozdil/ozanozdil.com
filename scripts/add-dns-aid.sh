#!/usr/bin/env bash
set -e

API_TOKEN="$1"
ZONE_ID="a799b528585cf824157dae9effba4fa1"

if [ -z "$API_TOKEN" ]; then
  echo "Kullanım: ./scripts/add-dns-aid.sh <CLOUDFLARE_API_TOKEN>"
  exit 1
fi

echo "1/3: _index._agents.ozanozdil.com (HTTPS) ekleniyor..."
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
     -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{
       "type": "HTTPS",
       "name": "_index._agents.ozanozdil.com",
       "data": {
         "priority": 1,
         "target": "www.ozanozdil.com",
         "value": "alpn=\"h2,h3\" port=443"
       },
       "ttl": 3600
     }' | jq -r '.success, (.errors[]?.message // "OK")'

echo "2/3: _a2a._agents.ozanozdil.com (SVCB) ekleniyor..."
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
     -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{
       "type": "SVCB",
       "name": "_a2a._agents.ozanozdil.com",
       "data": {
         "priority": 1,
         "target": "www.ozanozdil.com",
         "value": "alpn=\"a2a\" port=443 mandatory=alpn,port"
       },
       "ttl": 3600
     }' | jq -r '.success, (.errors[]?.message // "OK")'

echo "3/3: _mcp._agents.ozanozdil.com (SVCB) ekleniyor..."
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
     -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{
       "type": "SVCB",
       "name": "_mcp._agents.ozanozdil.com",
       "data": {
         "priority": 1,
         "target": "www.ozanozdil.com",
         "value": "alpn=\"h2,h3\" port=443"
       },
       "ttl": 3600
     }' | jq -r '.success, (.errors[]?.message // "OK")'

echo "Tamamlandı!"
