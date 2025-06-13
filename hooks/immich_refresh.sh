#!/bin/bash
# Refresh Immich after new file import
curl -X POST http://immich-server:3000/api/jobs/refresh-api \
     -H "Authorization: Bearer $IMMICH_API_KEY"
