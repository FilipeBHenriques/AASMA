import asyncio
import time
import sys

from poke_env.player import RandomPlayer, ReactivePlayer, ProactivePlayer
from poke_env import LocalhostServerConfiguration, PlayerConfiguration
from poke_env.teambuilder.gen1ou_team import Team

n_battles = 0
if len(sys.argv) > 1:
    try:
        n_battles = int(sys.argv[1])
    except ValueError:
        print("Invalid integer provided.")
else:
    print("No integer provided as an argument.")

def print_dict(dict):
    win_rate = dict["win_rate"]*100
    print(f"Win Rate: {win_rate:.2f} %")
    print("Average Number of Turns: " + str(float(dict["battle_duration_avg"])) + " turns")
    print("Average Pokemon alive: " + str(float(dict["pokemon_alive_avg"])))

async def main_battle(player1, player2, n_battles):
    battle_number = 0
    n = 0
    threshold = time.time()
    battle_duration_total = 0
    pokemon_alive_total = 0
    for _ in range(n_battles):
        if battle_number % 50 == 0:
            print(str(battle_number) + "/" + str(n_battles))
        if n == 5 and (time.time() - threshold) < 181:
            time.sleep(210 - (time.time() - threshold))
            n = 0
            threshold = time.time()
        elif n == 5:
            n = 0
            threshold = time.time()
        else:
            await player1.battle_against(player2, 1)
            n += 1
        battle_number+=1     

    for battle in player1._battles.values():
        print(battle._turn)
        battle_duration_total += battle._turn
        pokemon_alive = len(battle.available_switches)
        if "FNT" not in str(battle.active_pokemon._status):
            pokemon_alive += 1
        pokemon_alive_total += pokemon_alive
        print(pokemon_alive_total)
    
    metrics = {
        "win_rate": player1.n_won_battles / n_battles,
        "battle_duration_avg": float(battle_duration_total / n_battles),
        "pokemon_alive_avg": float(pokemon_alive_total / n_battles)
    }

    return metrics

async def main():
    # We create three players.
    random_player = RandomPlayer(
        player_configuration=PlayerConfiguration("random-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou",
        team=Team.pick_random_team(),
    )

    reactive_player = ReactivePlayer(
        player_configuration=PlayerConfiguration("reactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou",
        team=Team.pick_random_team(),
    )

    proactive_player = ProactivePlayer(
        player_configuration=PlayerConfiguration("proactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou",
        team=Team.pick_random_team(),
    )

    start = time.time()
    reactive_metrics = await main_battle(reactive_player, random_player, n_battles)
    print(
        "\n%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Reactive Player", reactive_player.n_won_battles, n_battles, time.time() - start)
    )

    print("\nMetrics for Reactive Player against RandomPlayer:")
    print_dict(reactive_metrics)

    ##########################################################################################

    start = time.time()
    proactive_metrics = await main_battle(proactive_player, random_player, n_battles)
    print(
        "\n%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Proactive Player", proactive_player.n_won_battles, n_battles, time.time() - start)
    )

    print("\nMetrics for Proactive Player against RandomPlayer:")
    print_dict(proactive_metrics)

    ##########################################################################################

    reactive_player.reset_battles()
    proactive_player.reset_battles()
    start = time.time()
    proactive_metrics_against_reactive = await main_battle(proactive_player, reactive_player, n_battles)

    print("##########################################################################################")

    print(
        "\n%s won %d / %d battles against the Reactive Player [this took %f seconds]"
        % (
            "Proactive Player",
            proactive_player.n_won_battles,
            n_battles,
            time.time() - start,
        )
    )

    print(
        "%s won %d / %d battles against the Proactive Player [this took %f seconds]"
        % (
            "Reactive Player",
            reactive_player.n_won_battles,
            n_battles,
            time.time() - start,
        )
    )    

    print("\nMetrics for Proactive Player against Reactive Player:")
    print_dict(proactive_metrics_against_reactive)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())    