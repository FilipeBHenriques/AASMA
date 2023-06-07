"""This module defines a reactive agent AI
"""

from math import floor
import random
from poke_env.environment.battle import Battle
from poke_env.environment.pokemon import Pokemon
from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.move import Move

MAX_WEIGHT = 2048
debug = 1

movesetUsage = {}
movesetUsage["snorlax"]     = ["bodyslam", "selfdestruct", "earthquake", "hyperbeam", "reflect", "rest", "amnesia", 
                               "counter", "icebeam", "blizzard"]
movesetUsage["tauros"]      = ["bodyslam", "hyperbeam", "blizzard", "earthquake", "fireblast"]
movesetUsage["chansey"]     = ["softboiled", "thunderwave", "icebeam", "thunderbolt", "seismictoss", "reflect", 
                               "counter", "sing"]
movesetUsage["exeggutor"]   = ["psychic", "sleeppowder", "explosion", "stunspore", "doubleedge", "hyperbeam", "megadrain", 
                               "leechseed"]
movesetUsage["alakazam"]    = ["thunderwave", "psychic", "seismictoss", "recover", "reflect"]
movesetUsage["starmie"]     = ["thunderwave", "blizzard", "recover", "thunderbolt", "psychic"]
movesetUsage["jynx"]        = ["lovelykiss", "blizzard", "psychic", "rest"]
movesetUsage["zapdos"]      = ["thunderbolt", "drillpeck", "thunderwave", "agility", "thunder", "rest"]
movesetUsage["rhydon"]      = ["earthequake", "substitute", "rockslide", "bodyslam"]
movesetUsage["lapras"]      = ["blizzard", "thunderbolt", "confuseray", "sing", "bodyslam", "hyperbeam", "icebeam", 
                               "rest"]
movesetUsage["gengar"]      = ["hypnosis", "explosion", "nightshade", "thunderbolt", "seismictoss", "megadrain", 
                               "confuseray", "psychic"]
movesetUsage["golem"]       = ["earthquake", "explosion", "bodyslam", "rockslide", "substitute"]
movesetUsage["slowbro"]     = ["amnesia", "thunderwave", "surf", "rest", "psychic", "reflect", "blizzard"]
movesetUsage["jolteon"]     = ["thunderbolt", "thunderwave", "doublekick", "pinmissile", "rest"]
movesetUsage["cloyster"]    = ["blizzard", "clamp", "explosion", "hyperbeam", "icebeam"]
movesetUsage["persian"]     = ["slash", "hyperbeam", "bubblebeam", "thunderbolt", "thunder"]
movesetUsage["articuno"]    = ["blizzard", "agility", "hyperbeam", "skyattack", "doubleedge", "reflect", "icebeam", 
                               "substitute"]
movesetUsage["dragonite"]   = ["wrap", "agility", "blizzard", "hyperbeam", "surf"]

sideEffects = {}
sideEffects["FRZ"] = ["blizzard", "icebeam"]
sideEffects["SLP"] = ["sing", "sleeppowder", "hypnosis", "lovelykiss"]
sideEffects["PAR"] = ["thunderwave", "stunspore", "thunderbolt", "thunder", "bodyslam"]
sideEffects["BRN"] = ["fireblast"]
sideEffects["PSN"] = ["toxic"]

class ProactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon

        me_moves_score = []
        switches_score = []

        available_moves = battle.available_moves
        available_switches = battle.available_switches
        type_chart = opp._data.type_chart
        if debug:
            self.print_turnInfo(battle, me, opp, available_moves, available_switches)

        if len(available_moves) == 1:
            return BattleOrder(available_moves[0])

        if len(available_moves) > 1:
            me_moves_score = self.score_available_moves(battle, 0, me, opp, available_moves, type_chart)
        switches_score = self.score_available_switches(battle, opp, available_switches, type_chart)

        plays_highest_score = 0
        highest_scoring_play = None

        if len(available_moves) > 1:
            for i in range(len(available_moves)):
                if me_moves_score[i][1] > plays_highest_score:
                    plays_highest_score = me_moves_score[i][1]
                    highest_scoring_play = me_moves_score[i][0]

        for i in range(len(available_switches)):
            if switches_score[i][1] > plays_highest_score:
                plays_highest_score = switches_score[i][1]
                highest_scoring_play = switches_score[i][0]

        if debug:
            print(highest_scoring_play)
        if(highest_scoring_play == None):
            return self.choose_random_move(battle)
        return BattleOrder(highest_scoring_play)
    
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
            print(available_switch.species, available_switch._status, int((available_switch._current_hp/available_switch.max_hp)*100), str([move for move in available_switch._moves]))
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

    def score_available_moves(self, battle, is_switch, me, opp, available_moves, type_chart):
        me_moves_score = []

        me_recovery_tag = self.recovery(available_moves)
        me_outspeed_tag = self.outspeed(me, opp)
        
        opp_max_damage = self.opp_max_damage(battle, me, opp, type_chart)

        me_current_hp = (me._current_hp/me.max_hp)*100-(1+me_outspeed_tag)*opp_max_damage*is_switch
        if debug:
            print(f"{me.species}'s moves score (me_current_hp: {me_current_hp:.2f}, opp_max_damage: {opp_max_damage:.2f}, me_outspeed_tag: {me_outspeed_tag}):")
        
        for move in available_moves:
            move_info = move._moves_dict[move._id]

            category = move_info["category"]

            move_damage = 0
            stab = 1
            if category != "Status" and "SLP" not in str(me._status) and "FRZ" not in str(me._status) :
                if move._id == "seismictoss" or move._id == "nightshade":
                    move_damage = 100

                else:
                    if category == "Physical":
                        attack_stat = floor((me.base_stats["atk"]+15)*2+252/4)+5
                        defense_stat = floor((opp.base_stats["def"]+15)*2+252/4)+5
                        
                    else:
                        attack_stat = floor((me.base_stats["spa"]+15)*2+252/4)+5
                        defense_stat = floor((opp.base_stats["spd"]+15)*2+252/4)+5

                    move_type = move_info["type"].upper()
                    if move_type == me._type_1.name:
                        stab = 1.5
                    elif me._type_2 is not None and move_type == me._type_2.name:
                        stab = 1.5

                    type_effectiveness = type_chart[opp._type_1.name.upper()][move_type]
                    if opp._type_2 is not None:
                        type_effectiveness *= type_chart[opp._type_2.name.upper()][move_type]

                    move_damage = self.calculate_damage(100, attack_stat, defense_stat, move_info["basePower"], stab, type_effectiveness)

                opp_max_hp = floor((opp.base_stats["hp"]+15)*2+252/4)+110
                move_damage = move_damage/opp_max_hp*100

            move_acc = move_info["accuracy"]/100

            move_side_effect_value = 0
            move_side_effect_chance = 1
            if opp._status is None:
                if move_info["secondary"] is not None:
                    move_side_effect_chance = move_info["secondary"]["chance"]/100
                if move._id in sideEffects["FRZ"]:
                    move_side_effect_value = 100*move_side_effect_chance
                    for pokemon in battle.opponent_team.values():
                        if "FRZ" in str(pokemon._status):
                            move_side_effect_value = 0
                elif move._id in sideEffects["SLP"]:
                    move_side_effect_value = 90*move_side_effect_chance
                    for pokemon in battle.opponent_team.values():
                        if "SLP" in str(pokemon._status):
                            move_side_effect_value = 0
                elif move._id in sideEffects["PAR"]:
                    move_side_effect_value = 50*move_side_effect_chance
                elif move._id in sideEffects["BRN"] or move._id in sideEffects["PSN"]:
                    move_side_effect_value = 20*move_side_effect_chance

                move_side_effect_value *= move_side_effect_chance

            move_recoil = 0
            if move._id == "doubleedge":
                move_recoil = (move_damage/4)/me.max_hp*100
            elif move._id == "selfdestruct" or move._id == "explosion":
                move_recoil = me_current_hp

            move_recovery = 0
            if move._id == "recover" or move._id == "softboiled":
                move_recovery = 50
                if opp_max_damage < move_recovery and me_current_hp < 66:
                    move_side_effect_value = MAX_WEIGHT
            elif move._id == "rest":
                move_recovery = 100
                if opp_max_damage < move_recovery and me_current_hp < 50:
                    move_side_effect_value = MAX_WEIGHT

            move_score = max(me_current_hp-opp_max_damage, 1)/100*(1+me_outspeed_tag)*(move_damage+move_side_effect_value)*move_acc/min(opp_max_damage+move_recoil+1, 100)
            if me_recovery_tag == 1 and "SLP" not in str(opp._status) and "FRZ" not in str(opp._status):
                move_score *= 50/(opp_max_damage+1)
            if move_damage > opp._current_hp:
                move_is_free = me_outspeed_tag+int("FRZ" in str(opp._status))+int("SLP" in str(opp._status))
                move_score += MAX_WEIGHT*move_is_free*(1-is_switch)+100/move_info["basePower"]
            elif move._id == "hyperbeam":
                move_score *= 0.1

            if debug:
                print(f"\t{move._id} (move_damage: {move_damage:.2f}, move_side_effect_value: {move_side_effect_value}, move_acc: {move_acc:.2f}, move_recoil: {move_recoil:.2f}, move_score: {move_score:.2f})")
            move_score_data = [move, move_score]
            me_moves_score.append(move_score_data)

        return me_moves_score

    def score_available_switches(self, battle, opp, available_switches, type_chart):
        switches_score = []

        for switch in available_switches:
            switch_moves_score = []
            switch_available_moves = [switch._moves[move] for move in switch._moves]

            switch_moves_score = self.score_available_moves(battle, 1, switch, opp, switch_available_moves, type_chart)

            switchs_move_highest_score = 0
            for i in range(len(switch_available_moves)):
                if switch_moves_score[i][1] > switchs_move_highest_score:
                    switchs_move_highest_score = switch_moves_score[i][1]
            
            if debug:
                print(f"\t{switch.species}'s score = {switchs_move_highest_score}\n")
            switch_score_data = [switch, switchs_move_highest_score]
            switches_score.append(switch_score_data)

        return switches_score

    def outspeed(self, me, opp):
        if me.base_stats["spe"] > opp.base_stats["spe"]:
            outspeed = 1
        else:
            outspeed = 0
        if "PAR" in str(opp._status) and "PAR" not in str(me._status):
            outspeed = 1
        if "PAR" in str(me._status) and "PAR" not in str(opp._status):
            outspeed = 0
        return outspeed
    
    def recovery(self, available_moves):
        for move in available_moves:
            if move._id == "softboiled" or move._id == "recover":
                recovery = 1
            else:
                recovery = 0
        return recovery

    def opp_max_damage(self, battle, me, opp, type_chart):
        opp_max_damage = 0
        if "SLP" in str(opp._status) or "FRZ" in str(opp._status) or opp.must_recharge:
            return opp_max_damage
        
        for move_id in movesetUsage[opp.species]:
            if len(battle.available_moves) > 1:
                move_info = battle.available_moves[0]._moves_dict[move_id]
            else: 
                move_info = list(battle.available_switches[0]._moves.values())[0]._moves_dict[move_id]

            category = move_info["category"]
            if category == "Physical":
                attack_stat = floor((opp.base_stats["atk"]+15)*2+252/4)+5
                defense_stat = floor((me.base_stats["def"]+15)*2+252/4)+5
            elif category == "Special":
                attack_stat = floor((opp.base_stats["spa"]+15)*2+252/4)+5
                defense_stat = floor((me.base_stats["spd"]+15)*2+252/4)+5
            else:
                continue
            base_power = move_info["basePower"]
            move_type = move_info["type"].upper()
            if move_type == opp._type_1.name:
                stab = 1.5
            elif opp._type_2 is not None and move_type == opp._type_2.name:
                stab = 1.5
            else:
                stab = 1
            type_effectiveness = type_chart[me._type_1.name][move_type]
            if me._type_2 is not None:
                type_effectiveness *= type_chart[me._type_2.name][move_type]

            move_damage = self.calculate_damage(100, attack_stat, defense_stat, base_power, stab, type_effectiveness)
            move_damage = move_damage/me.max_hp*100
            if move_damage > opp_max_damage:
                opp_max_damage = move_damage
        
        return opp_max_damage

    def calculate_damage(self, level, attack_stat, defense_stat, base_power, stab, type_effectiveness):
        damage = (((2*level)/5+2)*base_power*attack_stat/defense_stat)/50+2
        damage *= stab
        damage *= type_effectiveness
        return int(damage)
