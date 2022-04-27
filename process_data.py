#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import numpy as np
import pandas as pd


# In[2]:


cards = pd.read_json('cards.json')
cards.drop(columns=['description', 'arena'], inplace=True)
cards = cards.set_index('key')


# In[3]:


cards


# In[4]:


cards.to_csv('data/cards.csv')


# In[5]:


with open('cards_stats.json') as file:
    cards_stats_full = json.load(file)
# print(cards_stats_full['characters'][0])


# In[6]:


name_to_key = {}
for i in cards_stats_full:
    for j in cards_stats_full[i]:
        if 'key' in j:
            name_to_key[j['name']] = {j['key']}
            if 'summon_character' in j:
                if j['summon_character'] not in name_to_key:
                    name_to_key[j['summon_character']] = {j['key']}
                else:
                    name_to_key[j['summon_character']].add(j['key'])


# In[7]:


cards_by_key = {i: {} for i in cards.index.values}
cards_by_name = {}
for i in cards_stats_full:
#     print('---------------------------')
#     print(i)
#     print('------')
#     print(cards_stats_full[i][0].keys())
#     print('---------------------------')
    for j in cards_stats_full[i]:
        name = j['name']
        cards_by_name[name] = j
        
        if name in name_to_key:
            for k in name_to_key[name]:
                if k is not None:
                    cards_by_key[k] = {**j, **cards_by_key[k]}

            
        if 'key' in j:
            if j['key'] in cards_by_key:
                cards_by_key[j['key']] = {**cards_by_key[j['key']] , **j}
            else:
                cards_by_key[j['key']] = j


# In[ ]:





# In[8]:


detail = {}
missing = {}
for i in cards.index.values:
    if len(cards_by_key[i]) != 0:
        detail[i] = cards_by_key[i]
    else:
        detail[i] = None
        missing[i] = None
missing


# In[9]:


missing['elixir-collector'] = 'ElixirCollector'
missing['fireball'] = 'FireballSpell'
missing['arrows'] = 'ArrowsSpell'
missing['rocket'] = 'RocketSpell'
missing['goblin-barrel'] = 'GoblinBarrelSpell'
missing['the-log'] = 'LogProjectile'
missing['giant-snowball'] = 'SnowballSpell'
missing['barbarian-barrel'] = 'BarbLogProjectile'

for i in missing:
    if missing[i] is not None:
        detail[i] = cards_by_name[missing[i]]


# In[10]:


detail['knight']['attacks_ground']


# In[11]:


def add_attribute(att):
    cards[att] = np.nan
    for i in cards.index.values:
        if detail[i] is not None and att in detail[i]:
            cards.loc[i, att] = detail[i][att]
    return cards


# In[12]:


attributes = {'range', 'attacks_ground', 'attacks_air', 'flying_height', 'hits_ground', 'hits_air', 'aoe_to_ground', 'aoe_to_air'}
for i in attributes:
    add_attribute(i)


# In[13]:


cards.fillna(False, inplace=True)
cards['range'] = cards['range'].astype(int)
cards['flying_height'] = cards['flying_height'].astype(int)
cards['damage_air'] = cards['hits_air'] | cards['attacks_air'] | cards['aoe_to_air']
cards['damage_ground'] = cards['hits_ground'] | cards['attacks_ground'] | cards['aoe_to_ground']
cards.drop(columns=['hits_air', 'attacks_air', 'aoe_to_air', 'hits_ground', 'attacks_ground', 'aoe_to_ground'], inplace=True)


# In[14]:


cards


# In[15]:


cards.to_csv('data/cards.csv')


# In[16]:


import os
for i in os.walk('battles'):
    _, _, files = i


# In[17]:


players = []
for filename in files:
    with open(f'battles/{filename}') as file:
        players.append(json.load(file))
len(players)


# In[18]:


# print(players[0][10].keys())


# In[ ]:





# In[19]:


# print(players[0][10]['team'][0]['cards'][0].keys())


# In[20]:


# files[0]


# In[21]:


def add_battle(battles, b):
    assert(len(b['team']) == 1)
    assert(len(b['opponent']) == 1)
    team = b['team'][0]
    op = b['opponent'][0]
    tmp = {}
    
    for p, info in enumerate([team, op]):
        player = p + 1
        tmp[f'p{player}_tag'] = info['tag']
        tmp[f'p{player}_trophy'] = info['startingTrophies']
        for i, c in enumerate(info['cards']):
            tmp[f'p{player}_card_{i}_id'] = c['id']
            tmp[f'p{player}_card_{i}_lv'] = c['level']
        tmp[f'p{player}_crowns'] = info['crowns']
    tmp['winner'] =  1 if team['crowns'] > op['crowns'] else (2 if team['crowns'] < op['crowns'] else 0)
    battles.append(tmp)
    


# In[22]:


battles = []
types_filter = {'PvP'}
card_info_filter = {'id', 'name', 'level'}
for player in players:
    for battle in player:
        if battle['type'] in types_filter:
            add_battle(battles, battle)
            


# In[23]:


battle_df = {i: [] for i in battles[0].keys()}
for i in battles:
    for k in battle_df:
        battle_df[k].append(i[k])
    


# In[24]:


battle_df = pd.DataFrame.from_dict(battle_df)


# In[25]:


battle_df


# In[26]:


battle_df.to_csv('data/battles.csv')

