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
sideEffects["BRN"] = ["firblast"]
sideEffects["PSN"] = ["toxic"]


class ReactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        me = battle.active_pokemon
        opp = battle.opponent_active_pokemon
        
        available_moves = battle.available_moves

        typeMatchup = self.getWeaknesses(battle)

        print("***************************************************************************************************")
        print("[Turn ", battle._turn, "]")
        print("OPPONENT Pokemon:", opp.species, opp._status, opp._current_hp, opp.base_stats)
        print("ME Active Pokemon:", me.species, me._status, int((me._current_hp/me.max_hp)*100), me.base_stats["spe"], str([move._id for move in available_moves]))

        best_move = self.evaluate_available_moves(available_moves, battle, me, opp)

        print("Chosen_move -> ", best_move)

        self.print_team_moves(battle)
        self.print_Weak_Resis_Immun(typeMatchup)

        return BattleOrder(best_move)
    
    def getSideEffectsMove(self, move):
        sideEffectVal = 0
        if move._id in sideEffects["FRZ"]:
            sideEffectVal = 100
        elif move._id in sideEffects["SLP"]:
            sideEffectVal = 90
        elif move._id in sideEffects["PAR"]:
            sideEffectVal = 50
        elif move._id in sideEffects["BRN"] or move._id in sideEffects["PSN"]:
            sideEffectVal = 20
        return sideEffectVal
    
    def get_outspeed(self, me, opp):
        if me.base_stats["spe"] > opp.base_stats["spe"]:
            outspeed = 1
        else:
            outspeed = 0
        return outspeed
    
    def get_reliable_recovery(self, available_moves):
        for move in available_moves:
            if move._id == "softboiled" or move._id == "recover":
                reliableRecovery = 1
            else:
                reliableRecovery = 0
        return reliableRecovery
    
    def evaluate_available_moves(self, available_moves, battle, me, opp):
        opp_max_hp = floor((opp.base_stats["hp"]+15)*2+252/4)+110
        max_score = 0
        if available_moves:
            best_move = available_moves[0]
            outspeed = self.get_outspeed(me, opp)
            oppMaxDmg = self.get_opponent_strongest_move_damage(me, opp, battle)
            for move in available_moves:
                move_info = battle.available_moves[0]._moves_dict[move._id]
                acc = move_info["accuracy"]
                if move._id == "softboiled" or move._id == "recover" or move._id == "rest":
                    #placeholder
                    score = 0
                elif move._id == "amnesia" or move._id == "reflect" or move._id == "agility":
                    #placeholder
                    score = 0
                elif move._id == "explosion" or move._id == "selfdestruct" or move._id == "hyperbeam" or move._id == "doubleedge":
                    #placeholder
                    score = 0
                elif move._id == "seismictoss" or move._id == "nightshade":
                    move_dmg = 100/opp_max_hp*100
                    score_baseline = ((me._current_hp/me.max_hp)*100-oppMaxDmg)/100*(move_dmg)*(acc/100)/(oppMaxDmg+1)
                    #add recovery impact
                    if move_dmg > opp._current_hp:
                        outspeed_benefit = outspeed*MAX_WEIGHT
                    else:
                        outspeed_benefit = 0
                    
                    score = score_baseline+outspeed_benefit
                else:
                    score = self.calculate_normal_move_score(move, move_info, me, opp, opp_max_hp, oppMaxDmg, outspeed)

                print("[", move._id, "] (", score, ")")
                if score > max_score:
                    max_score = score
                    best_move = move
        else: #pokemon morreu -> obrigatório dar switch
            best_move = battle.available_switches[random.randint(0, len(battle.available_switches)-1)]

        return best_move

    def calculate_damage(self, level, attack_stat, defense_stat, base_power, stab, type_effectiveness):
        damage = (((2*level)/5+2)*base_power*attack_stat/defense_stat)/50+2
        damage *= stab
        damage *= type_effectiveness
        return int(damage)

    def get_opponent_strongest_move_damage(self, me, opp, battle):
        type_chart = opp._data.type_chart
        biggest_damage = 0
        for move_id in movesetUsage[opp.species]:
            move_info = battle.available_moves[0]._moves_dict[move_id]
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

            damage = self.calculate_damage(100, attack_stat, defense_stat, base_power, stab, type_effectiveness)
            damage = damage/me._current_hp*100
            #print(move_id, stab, type_effectiveness, damage)
            if damage > biggest_damage:
                biggest_damage = damage
        
        return biggest_damage

    def calculate_normal_move_score(self, move, move_info, me, opp, opp_max_hp, oppMaxDmg, outspeed):
        outspeed = self.get_outspeed(me, opp)
        type_chart = opp._data.type_chart
        acc = move_info["accuracy"]
        category = move_info["category"]
        if category == "Status":
            move_dmg = 0
        else:
            if category == "Physical":
                attack_stat = floor((me.base_stats["atk"]+15)*2+252/4)+5
                defense_stat = floor((opp.base_stats["def"]+15)*2+252/4)+5
            else:
                attack_stat = floor((me.base_stats["spa"]+15)*2+252/4)+5
                defense_stat = floor((opp.base_stats["spd"]+15)*2+252/4)+5
            move_type = move_info["type"].upper()
            if move_type == me._type_1:
                stab = 1.5
            elif me._type_2 is not None and move_type == me._type_2:
                stab = 1.5
            else:
                stab = 1
            type_effectiveness = type_chart[opp._type_1.name][move_type]
            if opp._type_2 is not None:
                type_effectiveness *= type_chart[opp._type_2.name][move_type]
            move_dmg = self.calculate_damage(100, attack_stat, defense_stat, move_info["basePower"], stab, type_effectiveness)
            move_dmg = move_dmg/opp_max_hp*100
            #print(move._id, stab, type_effectiveness, move_dmg)

        sideEffectsVal = 0
        if opp._status is None:
            sideEffectsVal = self.getSideEffectsMove(move)

        score_baseline = ((me._current_hp/me.max_hp)*100-oppMaxDmg)/100*(move_dmg+sideEffectsVal)*(acc/100)/(oppMaxDmg+1)
        ##add recovery impact
        if move_dmg > opp._current_hp:
            outspeed_benefit = outspeed*MAX_WEIGHT
        else:
            outspeed_benefit = 0
        score = score_baseline+outspeed_benefit
        return score

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

    def find_strongest_super_effective_move(self, battle, weakArr, moves):
        best_moves = []
        for weak_type in weakArr:
            for move in moves:
                #if move._id != "selfdestruct" or len(battle.available_switches) > 1:
                    #if move._id != "counter" and move._id != "nightshade" and move._id != "seismictoss":
                        move_type = PokemonType[move.entry["type"].upper()]._name_
                        if move_type == weak_type[0]:
                            move_base_power = move.entry.get("basePower", 0)
                            print("Move -> " + str(move._id) + "| type: " + str(move_type) + "| dmg: " + str(move_base_power))
                            best_moves.append((move, move_base_power*weak_type[1]))
        if best_moves:
            return sorted(best_moves, key=lambda x: x[1], reverse=True)
        return None
    
    def find_best_switch(self, battle: Battle, weakArr):
        moves_after_switch = []
        for pokemon in battle.available_switches:
            #print("Switch to -> " + str(pokemon) + " with moves: " + str(list(pokemon.moves.values())))
            moves_after_switch.append((pokemon, self.find_strongest_super_effective_move(battle, weakArr, list(pokemon.moves.values()))))
        moves_after_switch = [(pokemon, move) for pokemon, move in moves_after_switch if move is not None]
        if moves_after_switch:
            return self.get_best_switch(moves_after_switch)
        return None

    def get_best_switch(self, moves_after_switch):
        best_switch = (moves_after_switch[0][0], moves_after_switch[0][0].current_hp, moves_after_switch[0][1][0][1])
        for pokemon_moves in moves_after_switch:
            max_dmg_move = pokemon_moves[1][0][1]
            if max_dmg_move > best_switch[2]:# and self.check_if_pokemon_has_effects(pokemon_moves[0]) is False:
                best_switch = (pokemon_moves[0], pokemon_moves[0].current_hp, max_dmg_move)
        return best_switch
    
    def print_Weak_Resis_Immun(self, typeMatchup):
        print("\nWeaknesses: ", typeMatchup[0])
        print("Resistances: ", typeMatchup[1])
        print("Immunities: ", typeMatchup[2])
        print("***************************************************************************************************")

    def print_team_moves(self, battle):
        print("\nBenched Pokemon:")
        for available_switch in battle.available_switches:
            print(available_switch.species, available_switch._status, str([move for move in available_switch._moves]))
       
