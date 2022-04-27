#!/bin/bash

echo "Downloading cards"

# download cards and stats
curl https://royaleapi.github.io/cr-api-data/json/cards.json > ./cards.json
curl https://royaleapi.github.io/cr-api-data/json/cards_stats.json > ./cards_stats.json