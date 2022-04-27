#!/bin/bash

# put your API key from https://developer.clashroyale.com/#/ in apikey.txt
API_KEY=$(cat apikey.txt)

PLAYER=$1

readarray -t players < ./start_crawl.txt

PLAYER_LIMIT=${#players[@]}

echo "Fetching players"
i=1
for player in "${players[@]}"
do
	let i++
	FILENAME=$(echo $player | cut -d '#' -f 2)
	curl -H "Authorization: Bearer $API_KEY" "https://api.clashroyale.com/v1/players/%23$FILENAME/battlelog" > players.json 2> /dev/null
	cat players.json | tr ',' '\n' | grep 'opponent' | tr '"' '\n' | grep '#' >> players.txt
done
printf '\n'

# count how many players were downloaded
echo "$(ls ./battles | wc -l) players downloaded"

./fetch_scripts/fetch_cards.sh
./fetch_scripts/fetch_matches.sh