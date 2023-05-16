import asyncio
import numpy as np

from poke_env.player import cross_evaluate, RandomPlayer
from poke_env import LocalhostServerConfiguration, PlayerConfiguration
from poke_env.teambuilder import Teambuilder


class RandomTeamFromPool(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)

team_1 = """
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

Chansey (F)  
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

Tauros (M)  
Ability: none  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Earthquake  
"""

team_2 = """
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

Chansey (F)  
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

Tauros (M)  
Ability: none  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Earthquake  
"""

custom_builder = RandomTeamFromPool([team_1, team_2])