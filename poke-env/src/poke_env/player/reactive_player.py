"""This module defines a reactive agent AI
"""

import random
from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.pokemon_type import PokemonType


class ReactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        arrays = self.getWeaknesses(battle)
        weakArr = arrays[0]
        resiArr = arrays[1]
        immuArr = arrays[2]
        moves_team = self.getAllMovesTeam(battle)
        self.print_Weak_Resis_Immun(battle, arrays)
        self.print_team_moves(moves_team)

        #move.type move.base_power
        best_move = self.find_max_effective_move(weakArr, moves_team)
        if best_move != None:
            print("Move -> ", best_move)
            return best_move
        else:
            #implementar aqui o choose_effective_ switch
            switches = [BattleOrder(switch) for switch in battle.available_switches]
            return switches[int(random.random() * len(switches))]
    
    def find_max_effective_move(self, weakArr, moves_team):
        for weak_type in weakArr:
            #print("WeakType -> ", weak_type)
            for move in moves_team[0][1]:
                move_type = PokemonType[move.entry["type"].upper()]._name_
                move_base_power = move.entry.get("basePower", 0)
                #print("BasePower = ", move_base_power)
                #print("Move -> " + str(move._id) + "| type: " + str(move_type))
                if str(move_type) == weak_type[0] and move_base_power > 0:
                    return BattleOrder(move)

    def print_Weak_Resis_Immun(self, battle, arrays):
        print("\n")
        print("Opponent [" + str(battle.opponent_active_pokemon.species) +"] is: ")
        print("Weak against -> " + str(arrays[0]))
        print("Resistant against -> " + str(arrays[1]))
        print("Immune against -> " + str(arrays[2]) + "\n")

    def print_team_moves(self, moves):
        print("Team available moves")
        #print(str(moves[0][0]) + "-> " + str([m._id for m in moves[0][1]]))
        print(str(moves[0][0]) + "-> " + str([m._id for m in moves[0][1]]))
        for move in moves[1:]:
            print(str(move[0]) + "-> " + str([m for m in move[1]]))
        print("#################################################")
