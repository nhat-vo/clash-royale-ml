#!/bin/bash

# put your API key from https://developer.clashroyale.com/#/ in apikey.txt
API_KEY=$(cat apikey.txt)

# params (check https://developer.clashroyale.com/#/documentation for more details)
LOCATION=57000255
PLAYER_LIMIT=100

# download cards and stats
curl https://royaleapi.github.io/cr-api-data/json/cards.json > cards.json
curl https://royaleapi.github.io/cr-api-data/json/cards_stats.json > cards_stats.json

# download top $PLAYER_LIMIT players
curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/locations/$LOCATION/rankings/players?limit=$PLAYER_LIMIT" | tr '"' '\n' | grep '#' > players.txt

# download battle logs from top players
readarray -t players < players.txt
rm -rf battles
mkdir battles

for player in "${players[@]}"
do
	FILENAME=$(echo $player | cut -d '#' -f 2)
	curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/players/%23$FILENAME/battlelog" > "./battles/$FILENAME.json" 2> /dev/null

	# remove players with empty battle logs
	if test $(du -k "./battles/$FILENAME.json" | cut -f 1) -lt 1
	then 
		rm -f "./battles/$FILENAME.json"
	fi
done

# count how many players were downloaded
echo "$(ls battles | wc -l) players downloaded"


