import asyncio
import time
import sys

from poke_env.player import ReactivePlayer, ProactivePlayer
from poke_env import LocalhostServerConfiguration, ShowdownServerConfiguration, PlayerConfiguration
from poke_env.teambuilder.gen1ou_team import Team
from poke_env.teambuilder.constant_teambuilder import ConstantTeambuilder

n_battles = 0
if len(sys.argv) > 1:
    try:
        n_battles = int(sys.argv[1])
    except ValueError:
        print("Invalid integer provided.")
else:
    print("No integer provided as an argument.")

handicap_reactive = 0
handicap_proactive = 0

if len(sys.argv) > 3:
    try:
        if int(sys.argv[2]) < 5 and int(sys.argv[3]):
            handicap_reactive = int(sys.argv[2])
            handicap_proactive = int(sys.argv[3])
    except ValueError:
        print("Invalid integer provided.")



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
    n = 0
    wins = 0
    loses = 0
    draws = 0
    threshold = time.time()
    battle_duration_total = 0
    pokemon_alive_total = 0
    pokemon_alive_total_opp = 0
    for _ in range(n_battles):
        print(f"{_+1}/{n_battles}")
        if handicap_reactive == 0:
            test_team_reactive = Team.pick_random_team()
        else:
            test_team_reactive = Team.pick_random_handicap_team(handicap_reactive)

        if handicap_proactive == 0:
            test_team_proactive = Team.pick_random_team()
        else:
            test_team_proactive = Team.pick_random_handicap_team(handicap_proactive)
        print(f"{_+1}/{n_battles}")
        if n == 5 and (time.time() - threshold) < 181:
            time.sleep(210 - (time.time() - threshold))
            n = 0
            threshold = time.time()
        elif n == 5:
            n = 0
            threshold = time.time()
        else:
            await player1.battle_against(player2, 1)
            if player1.n_won_battles == 1:
                wins += 1
            elif player2.n_won_battles == 1:
                loses += 1
            else:
                draws +=1
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
            n += 1
        if handicap_reactive == 0:
            test_team_reactive = Team.pick_random_team()
        else:
            test_team_reactive = Team.pick_random_handicap_team(handicap_reactive)

        if handicap_proactive == 0:
            test_team_proactive = Team.pick_random_team()
        else:
            test_team_proactive = Team.pick_random_handicap_team(handicap_proactive)

        player2.reset_battles()
        player1.reset_battles()
        player1._team = ConstantTeambuilder(test_team_proactive)
        player2._team = ConstantTeambuilder(test_team_reactive)  
    
    metrics = {
        "win_rate": wins / n_battles,
        "wins" : wins,
        "loses" : loses,
        "draws": draws,
        "battle_duration_avg": float(battle_duration_total / n_battles),
        "pokemon_alive_avg": float(pokemon_alive_total / n_battles),
        "pokemon_alive_avg_opp": float(pokemon_alive_total_opp / n_battles)
    }

    return metrics

async def main():
    # We create two players.
    if handicap_reactive == 0:
        test_team_reactive = Team.pick_random_team()
    else:
        test_team_reactive = Team.pick_random_handicap_team(handicap_reactive)

    if handicap_proactive == 0:
        test_team_proactive = Team.pick_random_team()
    else:
        test_team_proactive = Team.pick_random_handicap_team(handicap_proactive)

    reactive_player = ReactivePlayer(
        player_configuration=PlayerConfiguration("reactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=test_team_reactive)
    
    proactive_player = ProactivePlayer(
        player_configuration=PlayerConfiguration("proactive-agnt", "password"),
        server_configuration=LocalhostServerConfiguration,
        battle_format="gen1ou", 
        team=test_team_proactive)

    start = time.time()
    proactive_metrics = await main_battle(proactive_player, reactive_player, n_battles)
    print(
        "\n%s won %d / %d battles against the Reactive Player [this took %f seconds]"
        % ("Proactive Player", proactive_metrics["wins"], n_battles, time.time() - start)
    )

    print("\nMetrics for Proactive Player against Reactive Player:")
    print_dict(proactive_metrics, proactive_player._username, reactive_player._username)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
