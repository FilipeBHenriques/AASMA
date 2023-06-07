import random

teams = {}
teams[0] = """
Starmie  
Ability: none  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Psychic  
- Blizzard  
- Thunder Wave  
- Recover  

Exeggutor  
Ability: none  
- Sleep Powder  
- Psychic  
- Double-Edge  
- Explosion  

Alakazam  
Ability: none  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Psychic  
- Seismic Toss  
- Thunder Wave  
- Recover  

Chansey  
Ability: none  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Ice Beam  
- Thunderbolt  
- Thunder Wave  
- Soft-Boiled  

Snorlax  
Ability: none  
- Body Slam  
- Reflect  
- Earthquake  
- Rest  

Tauros  
Ability: none  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Earthquake  
"""

teams[1] = """
Gengar  
Ability: none  
- Hypnosis  
- Night Shade  
- Thunderbolt  
- Explosion  

Zapdos  
Ability: none  
- Thunderbolt  
- Drill Peck  
- Agility  
- Thunder Wave  

Articuno  
Ability: none  
- Blizzard  
- Agility  
- Double-Edge  
- Hyper Beam  

Chansey  
Ability: none  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Sing  
- Ice Beam  
- Counter  
- Soft-Boiled  

Snorlax  
Ability: none  
- Body Slam  
- Reflect  
- Self-Destruct  
- Rest  

Tauros 
Ability: none  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Earthquake  
"""

teams[2] = """
Jynx  
Ability: Oblivious  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Lovely Kiss  
- Blizzard  
- Psychic  
- Rest  

Starmie  
Ability: Illuminate  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Psychic  
- Blizzard  
- Thunder Wave  
- Recover  

Jolteon  
Ability: Volt Absorb  
- Thunderbolt  
- Thunder Wave  
- Double Kick  
- Rest  

Chansey  
Ability: Natural Cure  
EVs: 252 HP / 252 Def / 252 SpA / 252 SpD / 252 Spe  
IVs: 2 Atk  
- Ice Beam  
- Thunderbolt  
- Counter  
- Soft-Boiled  

Snorlax  
Ability: Immunity  
- Amnesia  
- Ice Beam  
- Reflect  
- Rest  

Tauros  
Ability: Intimidate  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Fire Blast 
"""

class Team():
    def pick_random_team():
        i = random.randint(0, 2)
        return teams[i]