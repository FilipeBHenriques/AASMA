import asyncio
import time

from poke_env.player import RandomPlayer, ReactivePlayer, ProactivePlayer
from poke_env import LocalhostServerConfiguration, PlayerConfiguration
from poke_env.teambuilder.gen1ou_team import Team


async def main_battle(player1, player2, n_battles):
    n = 0
    threshold = time.time()
    battle_duration_total = 0
    pokemon_alive_total = 0
    damage_dealt_total = 0
    damage_taken_total = 0

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
            battle_start = time.time()
            await player1.battle_against(player2, 1)
            battle_duration = time.time() - battle_start
            battle_duration_total += battle_duration

            #damage_dealt_total += player1._team[0].damage_dealt
            #damage_taken_total += player1._team[0].damage_taken
            pokemon_alive = sum(1 for pokemon in player1.player.team if pokemon.current_hp > 0)
            pokemon_alive_total += pokemon_alive
            n += 1

    metrics = {
        "win_rate": player1.n_won_battles / n_battles,
        "battle_duration_avg": battle_duration_total / n_battles,
        "pokemon_alive_avg": pokemon_alive_total / n_battles,
        "damage_dealt_total" : damage_dealt_total,
        "damage_taken_total" : damage_taken_total
    }

    return metrics

async def main():
    n_battles = 1
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
        "%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Reactive Player", reactive_player.n_won_battles, n_battles, time.time() - start)
    )

    ##########################################################################################

    start = time.time()
    proactive_metrics = await main_battle(proactive_player, random_player, n_battles)
    print(
        "%s won %d / %d battles against the RandomPlayer [this took %f seconds]"
        % ("Proactive Player", proactive_player.n_won_battles, n_battles, time.time() - start)
    )

    ##########################################################################################

    reactive_player.reset_battles()
    proactive_player.reset_battles()
    start = time.time()
    proactive_metrics_against_reactive = await main_battle(proactive_player, reactive_player, n_battles)

    print("##########################################################################################")

    print(
        "%s won %d / %d battles against the Reactive Player [this took %f seconds]"
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

    # Print collected metrics
    print("Metrics for Reactive Player:")
    print(reactive_metrics)

    print("Metrics for Proactive Player:")
    print(proactive_metrics)

    print("Metrics for Proactive Player against Reactive Player:")
    print(proactive_metrics_against_reactive)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())    