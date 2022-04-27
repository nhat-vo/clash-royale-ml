#!/bin/bash

# put your API key from https://developer.clashroyale.com/#/ in apikey.txt
API_KEY=$(cat apikey.txt)

PLAYER=$1
PLAYER_LIMIT=${2:-100}

curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/players/%23$PLAYER/battlelog" > "players.json" 2> /dev/null
cat players.json | tr ',' '\n' | grep 'opponent' | tr '"' '\n' | grep '#' > players.txt

./fetch_scripts/fetch_cards.sh
./fetch_scripts/fetch_matches.sh