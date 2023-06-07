from math import floor
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.pokemon_type import PokemonType


class ReactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        if len(battle.available_moves) == 1: #recharge
            return BattleOrder(battle.available_moves[0])
        if battle._force_switch:
            return BattleOrder(self.find_best_switch(battle))
        best_move, move_dmg = self.find_strongest_attack_move(battle, battle.available_moves)
        if move_dmg == 0:
            if len(battle.available_switches) == 0:
                return self.choose_random_singles_move(battle)
            else:
                return BattleOrder(self.find_best_switch(battle))
        return BattleOrder(best_move)

    def find_strongest_attack_move(self, battle, moves):
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon
        type_chart = opp._data.type_chart
        moves_dict = moves[0]._moves_dict
        best_move = moves[0]
        biggest_damage = 0
        for move in moves:
            move_info = moves_dict[move._id]
            category = move_info["category"]
            if category == "Physical":
                attack_stat = floor((me.base_stats["atk"]+15)*2+252/4)+5
                defense_stat = floor((opp.base_stats["def"]+15)*2+252/4)+5
            elif category == "Special":
                attack_stat = floor((me.base_stats["spa"]+15)*2+252/4)+5
                defense_stat = floor((opp.base_stats["spd"]+15)*2+252/4)+5
            else:
                continue
            base_power = move_info["basePower"]
            move_type = move_info["type"].upper()
            if move_type == me._type_1.name:
                stab = 1.5
            elif me._type_2 is not None and move_type == me._type_2.name:
                stab = 1.5
            else:
                stab = 1
            type_effectiveness = type_chart[opp._type_1.name][move_type]
            if opp._type_2 is not None:
                type_effectiveness *= type_chart[opp._type_2.name][move_type]

            damage = self.calculate_damage(100, attack_stat, defense_stat, base_power, stab, type_effectiveness)
            damage = damage/opp._current_hp*100
            if damage > biggest_damage:
                biggest_damage = damage
                best_move = move
        return best_move, biggest_damage
    
    def calculate_damage(self, level, attack_stat, defense_stat, base_power, stab, type_effectiveness):
        damage = (((2*level)/5+2)*base_power*attack_stat/defense_stat)/50+2
        damage *= stab
        damage *= type_effectiveness
        return int(damage)
    
    def find_best_switch(self, battle: Battle):
        moves_after_switch = []
        for pokemon in battle.available_switches:
            moves_after_switch.append((pokemon, self.find_strongest_attack_move(battle, list(pokemon.moves.values()))))
        best_switch = self.get_best_switch(moves_after_switch)
        return best_switch

    def get_best_switch(self, moves_after_switch):
        best_switch = (moves_after_switch[0][0], moves_after_switch[0][1][1])
        for pokemon in moves_after_switch:
            move_dmg = pokemon[1][1]
            if move_dmg > best_switch[1]:
                best_switch = (pokemon[0], pokemon[1][1])
        return best_switch[0]

    def print_turnInfo(self, battle, me, opp, available_moves, available_switches):
        typeMatchup = self.getWeaknesses(battle)
        weakArr = typeMatchup[0]
        resiArr = typeMatchup[1]
        immuArr = typeMatchup[2]

        print("***************************************************************************************************")
        print("[Turn ", battle._turn, "]")
        print("Active Pokemon:")
        print(me.species, me._status, int((me._current_hp/me.max_hp)*100), me.base_stats["spe"], str([move._id for move in available_moves]))
        print("Benched Pokemon:")
        for available_switch in available_switches:
            print(available_switch.species, available_switch._status, int((available_switch._current_hp/me.max_hp)*100), str([move for move in available_switch._moves]))
        print("Opponent Pokemon:")
        print(opp.species, opp._status, opp._current_hp, opp.base_stats["spe"])
        print("Weaknesses: ", weakArr)
        print("Resistances: ", resiArr)
        print("Immunities: ", immuArr)
        print("Opponent Benched Pokemon:")
        for pokemon in battle.opponent_team.values():
            if not pokemon.active:
                print(pokemon.species, pokemon._status)
        unknown = 6-len(battle.opponent_team.values())
        for i in range(unknown):
            print("UNKNOWN")
        print("***************************************************************************************************")
