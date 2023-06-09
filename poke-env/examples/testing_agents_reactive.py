import asyncio
import time
import sys

from poke_env.player import RandomPlayer, ReactivePlayer
from poke_env import LocalhostServerConfiguration, ShowdownServerConfiguration, PlayerConfiguration
from poke_env.teambuilder.gen1ou_team import Team

n_battles = 0
if len(sys.argv) > 1:
    try:
        n_battles = int(sys.argv[1])
    except ValueError:
        print("Invalid integer provided.")
else:
    print("No integer provided as an argument.")

handicap = 0

if len(sys.argv) > 2:
    try:
        if int(sys.argv[2]) < 5:
            handicap = int(sys.argv[2])
    except ValueError:
        print("Invalid integer provided.")

if handicap == 0:
    test_team = Team.pick_random_team()
else:
    test_team = Team.pick_random_handicap_team(handicap)

def print_dict(dict, name1, name2):
    win_rate = dict["win_rate"]*100
    print(f"Win Rate {name1} : {win_rate:.2f} %")
    print("Wins : " + str(dict["wins"]))
    print("Loses : " + str(dict["loses"]))
    print("Draws : " + str(dict["draws"]))
    print("Average Number of Turns: " + str(float(dict["battle_duration_avg"])) + " turns")
    print("Average Pokemon alive: " + str(float(dict["pokemon_alive_avg"])))
    print("Average Pokemon alive " + name2 + " : " + str(float(dict["pokemon_alive_avg_opp"])))

async def main_battle(player1, player2, n_battles):
    battle_number = 0
    n = 0
    threshold = time.time()
    battle_duration_total = 0
    pokemon_alive_total = 0
    pokemon_alive_total_opp = 0
    draws = 0
    for _ in range(n_battles):
        if n == 5 and (time.time() - threshold) < 181:
            time.sleep(210 - (time.time() - threshold))
            n = 0
            threshold = time.time()
        elif n == 5:
            n = 0
            threshold = time.time()
        else:
            battle_result = await player1.battle_against(player2, 1)
            if battle_result == "draw":
                draws +=1
            n += 1
        battle_number+=1     

    for battle in player1._battles.values():
        battle_duration_total += battle._turn
        pokemon_alive = len(battle.available_switches)
        if "FNT" not in str(battle.active_pokemon._status):
            pokemon_alive += 1
        pokemon_alive_total += pokemon_alive
    
    for battle in player2._battles.values():
        pokemon_alive_total_opp += len(battle.available_switches)
        if "FNT" not in str(battle.active_pokemon._status):
            pokemon_alive_total_opp += 1
    
    metrics = {
        "win_rate": player1.n_won_battles / n_battles,
        "wins" : player1.n_won_battles,
        "loses" : (n_battles - player1.n_won_battles - draws),
        "draws": draws,
        "battle_duration_avg": float(battle_duration_total / n_battles),
        "pokemon_alive_avg": float(pokemon_alive_total / n_battles),
        "pokemon_alive_avg_opp": float(pokemon_alive_total_opp / n_battles)
    }

    return metrics

async def main():
    # We create two players.
    random_player = RandomPlayer(
        player_configuration=PlayerConfiguration("random-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=Team.pick_random_team())
    
    reactive_player = ReactivePlayer(
        player_configuration=PlayerConfiguration("reactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=test_team)
    
    start = time.time()
    reactive_metrics = await main_battle(reactive_player, random_player, n_battles)

    print(
        "\n%s won %d / %d battles [this took %f seconds]"
        % ("Reactive Player", reactive_player.n_won_battles, n_battles, time.time() - start)
    )

    print("\nMetrics for Reactive Player against Random Player:")
    print_dict(reactive_metrics, reactive_player._username, random_player._username)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
