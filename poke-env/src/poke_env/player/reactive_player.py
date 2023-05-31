"""This module defines a reactive agent AI
"""

import random
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.pokemon_type import PokemonType


class ReactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon
        available_moves = battle.available_moves
        available_switches = battle.available_switches

        typeMatchup = self.getWeaknesses(battle)
        weakArr = typeMatchup[0]
        resiArr = typeMatchup[1]
        immuArr = typeMatchup[2]

        print("*********************************")
        print("[Turn ", battle._turn, "]")
        print("Active Pokemon:")
        print(me.species, me._status, me._current_hp, str([move._id for move in available_moves]))
        print("Benched Pokemon:")
        for available_switch in available_switches:
            print(available_switch.species, available_switch._status, str([move for move in available_switch._moves]))
        print("Opponent Pokemon:")
        print(opp.species, opp._status, opp._current_hp)
        print("Weaknesses: ", weakArr)
        print("Resistances: ", resiArr)
        print("Immunities: ", immuArr)
        
        moves_team = self.getAllMovesTeam(battle)
        best_moves = self.find_strongest_super_effective_move(weakArr, moves_team[0][1])
        if best_moves and self.check_if_pokemon_has_effects(battle.active_pokemon) is False:
            print("Move -> ", best_moves[0][0])
            return BattleOrder(best_moves[0][0]) 
        else:
            switch = self.find_best_switch(battle, weakArr)
            if switch:
                print("Switch -> ", switch[0])
                return BattleOrder(switch[0])
            else:
                """
                If the pokemon is less than half hp, switch to the highest hp pokemon that isn't weak against that oponnent
                else make the move with the highest move_base_power*resistance ratio
                """
                return self.choose_random_singles_move(battle)
    
    def check_if_pokemon_has_effects(self, pokemon:Pokemon):
        if pokemon._status:
            if "PAR" in str(pokemon._status):
                print("This pokemon is PAR")
                return True
            elif "SLP" in str(pokemon._status):
                print("This pokemon is SLP")
                return True
            elif "FRZ" in str(pokemon._status):
                print("This pokemon is FRZ")
                return True
            elif "BRN" in str(pokemon._status):
                print("This pokemon is BRN")
                return True
        return False

    def find_strongest_super_effective_move(self, weakArr, moves):
        best_moves = []
        for weak_type in weakArr:
            for move in moves:
                move_type = PokemonType[move.entry["type"].upper()]._name_
                if move_type == weak_type[0]:
                    move_base_power = move.entry.get("basePower", 0)
                    #print("BasePower = ", move_base_power)
                    #print("Move -> " + str(move._id) + "| type: " + str(move_type))
                    best_moves.append((move, move_base_power*weak_type[1]))
        if best_moves:
            return sorted(best_moves, key=lambda x: x[1], reverse=True)
        return None
    
    def find_best_switch(self, battle: Battle, weakArr):
        moves_after_switch = []
        for pokemon in battle.available_switches:
            #print("Switch to -> " + str(pokemon) + " with moves: " + str(list(pokemon.moves.values())))
            moves_after_switch.append((pokemon, self.find_strongest_super_effective_move(weakArr, list(pokemon.moves.values()))))
        moves_after_switch = [(pokemon, move) for pokemon, move in moves_after_switch if move is not None]
        if moves_after_switch:
            return self.get_best_switch(moves_after_switch)
        return None

    def get_best_switch(self, moves_after_switch):
        best_switch = (moves_after_switch[0][0], moves_after_switch[0][0].current_hp, moves_after_switch[0][1][0][1])
        for pokemon_moves in moves_after_switch:
            max_dmg_move = pokemon_moves[1][0][1]
            if max_dmg_move > best_switch[2] and self.check_if_pokemon_has_effects(pokemon_moves[0]) is False:
                best_switch = (pokemon_moves[0], pokemon_moves[0].current_hp, max_dmg_move)
        return best_switch
    
    def print_Weak_Resis_Immun(self, battle, typeMatchup):
        print("Opponent [" + str(battle.opponent_active_pokemon.species) +"] is: ")
        print("Weak against -> " + str(typeMatchup[0]))
        print("Resistant against -> " + str(typeMatchup[1]))
        print("Immune against -> " + str(typeMatchup[2]) + "\n")

    def print_team_moves(self, moves):
        print("Available teammates:")
        for move in moves[1:]:
            print(str(move[0]) + "-> " + str([m for m in move[1]]))
        print("#################################################")
