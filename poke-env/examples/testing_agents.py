import asyncio
import time

from poke_env.player import Player, RandomPlayer, ReactivePlayer
from poke_env import LocalhostServerConfiguration, ShowdownServerConfiguration, PlayerConfiguration


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

async def main():
    # We create two players.
    random_player_1 = RandomPlayer(
        player_configuration=PlayerConfiguration("aasmaClient1", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=team_1)
    
    random_player_2 = ReactivePlayer(
        player_configuration=PlayerConfiguration("aasmaClient0", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=team_2)
    start = time.time()

    # Now, let's evaluate our player
    #await random_player_1.battle_against(random_player_2, n_battles=100)
    n_battles = 5
    for _ in range(n_battles):
        await random_player_2.battle_against(random_player_1, 1)

    print(
        "%s won %d / %d battles [this took %f seconds]"
        % ("Reactive Player", random_player_2.n_won_battles, n_battles, time.time() - start)
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
