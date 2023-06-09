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
    
    def remove_random_member(string):
        # Split the string into sections
        sections = string.strip().split('\n\n')
        
        if len(sections) <= 1:
            # If there is only one section, return the original string
            return string
        
        # Select a random section to remove
        section_to_remove = random.choice(sections)
        
        # Remove the selected section from the list
        sections.remove(section_to_remove)
        
        # Join the remaining sections back into a string
        result = '\n\n'.join(sections)
        
        return result
    
    def pick_random_handicap_team(handicap):
        i = random.randint(0, 2)
        handicap_team = teams[i]

        for j in range(handicap):
            handicap_team = Team.remove_random_member(handicap_team)

        return handicap_team
