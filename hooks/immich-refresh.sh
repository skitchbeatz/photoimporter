#!/bin/bash
# Refresh Immich database after file import
curl -X POST "http://$IMMICH_SERVER/api/admin/scan" \
     -H "Authorization: Bearer $IMMICH_API_KEY" \
     -d "{\"path\": \"$1\"}"
