#!/bin/bash

# put your API key from https://developer.clashroyale.com/#/ in apikey.txt
API_KEY=$(cat apikey.txt)

# params (check https://developer.clashroyale.com/#/documentation for more details)
LOCATION=${2:-57000255}
PLAYER_LIMIT=${1:-100}


# download top $PLAYER_LIMIT players
curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/locations/$LOCATION/rankings/players?limit=$PLAYER_LIMIT" > players.json
cat players.json | tr ',' '\n' | grep -v 'clan' | tr '"' '\n' | grep '#' > players.txt


./fetch_scripts/fetch_cards.sh
./fetch_scripts/fetch_matches.sh
