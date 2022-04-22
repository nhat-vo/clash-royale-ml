#!/bin/bash
API_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjQzYzQ2MTliLTdiZWItNDNhZC05MTllLWE0NDA3MGVlZjlkYyIsImlhdCI6MTY1MDYxNDM4OSwic3ViIjoiZGV2ZWxvcGVyLzUxNzc1NDI1LTRiMTQtNDg0YS1kNzkzLTQ1ZmUzZTZiZjcyYiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjkuMTA0LjI1Mi42NiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.jVQj2xEifaRlOtPII04V6kdPGrsLbX7OgOHR_bOxEYZ6tNbXHG2pkYGjLAjE3RGQEGgLRHdJjIfF3e9-mvV8Sw'

curl https://royaleapi.github.io/cr-api-data/json/cards.json > cards.json
curl https://royaleapi.github.io/cr-api-data/json/cards_stats.json > cards_stats.json
curl -H "Authorization: Bearer $API_KEY" https://api.clashroyale.com/v1/locations/57000255/rankings/players?limit=100 | tr '"' '\n' | grep '#' > players.json

readarray -t players < players.json
for player in "${players[@]}"
do
# echo $player
FILENAME=$(echo $player | cut -d '#' -f 2)
# echo $FILENAME
curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/players/%23$FILENAME/battlelog" > "./battles/$FILENAME.json"
echo "https://api.clashroyale.com/v1/players/$player/battlelog"
done

