import asyncio
import time

from poke_env.player import RandomPlayer, ReactivePlayer, ProactivePlayer
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

async def main_battle(player1, player2, n_battles):
    n = 0
    threshold = time.time()
    for _ in range(n_battles):
        if n == 5 and (time.time() - threshold) < 181:
            print(time.time() - threshold)
            time.sleep(200 - (time.time() - threshold))
            n = 0
            threshold = time.time()
        elif n == 5:
            n = 0
            threshold = time.time()
        else:    
            await player1.battle_against(player2, 1)
            n+=1

async def main():
    n_battles = 1
    # We create three players.
    random_player = RandomPlayer(
        player_configuration=PlayerConfiguration("random-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=team_1)
    
    reactive_player = ReactivePlayer(
        player_configuration=PlayerConfiguration("reactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=team_2)
    
    proactive_player = ProactivePlayer(
        player_configuration=PlayerConfiguration("proactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=team_2)
    
    start = time.time()
    await main_battle(reactive_player, random_player, n_battles)
    print(
        "%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Reactive Player", reactive_player.n_won_battles, n_battles, time.time() - start)
    )

    ##########################################################################################

    start = time.time()
    await main_battle(proactive_player, random_player, n_battles)
    print(
        "%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Proactive Player", proactive_player.n_won_battles, n_battles, time.time() - start)
    )

    ##########################################################################################

    reactive_player.reset_battles()
    proactive_player.reset_battles()
    start = time.time()
    await main_battle(proactive_player, reactive_player, n_battles)
    
    print("##########################################################################################")

    print(
        "%s won %d / %d battles against the Reactive Player [this took %f seconds]"
        % ("Proactive Player", proactive_player.n_won_battles, n_battles, time.time() - start)
    )

    print(
        "%s won %d / %d battles against the Proactive Player [this took %f seconds]"
        % ("Reactive Player", reactive_player.n_won_battles, n_battles, time.time() - start)
    )

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



    
        
        