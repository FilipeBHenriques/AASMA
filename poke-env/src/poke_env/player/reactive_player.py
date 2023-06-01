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
        available_switches = battle.available_switches

        self.print_turnInfo(battle, me, opp, available_moves, available_switches)

        if len(available_moves) == 1:
            return BattleOrder(available_moves[0])
        
        '''begin{score_available_plays}'''
        type_chart = opp._data.type_chart
        opp_max_hp = floor((opp.base_stats["hp"]+15)*2+252/4)+110
        highestScore = 0
        '''begin{score_available_moves}'''
        oppDmg_onMe = self.get_opponent_strongest_move_damage(me, opp, battle)
        meOutspeed = self.outspeed(me, opp)
        meReliableRecovery = self.reliableRecovery(available_moves)
        print("---------------------------------------------------------------------------------------------------")
        print(f"{me.species.upper()}'s available move's score:")
        print(f"Max damage {opp.species.upper()} threatens {me.species.upper()} with: {oppDmg_onMe:.2f}")

        meCurrentHP_percentage = (me._current_hp/me.max_hp)*100
        highestScoringPlay, highestScore = self.getMovesScore(me, meCurrentHP_percentage, opp, available_moves, battle, opp_max_hp, meOutspeed, meReliableRecovery, oppDmg_onMe, type_chart, highestScore)
        '''end{score available moves}'''

        '''begin{score_available_switches}'''
        print("Available switches's score:")
        for switch in available_switches:
            switchScore = 0
            oppDmg_onSwitch = self.get_opponent_strongest_move_damage(switch, opp, battle)
            switchOutspeed = self.outspeed(switch, opp)
            switchReliableRecovery = self.reliableRecovery([switch._moves[move] for move in switch._moves])
            print(f"Max damage {opp.species.upper()} threatens {switch.species.upper()} with: {oppDmg_onSwitch:.2f}")
            
            switchHpAfterSwitchIn = (switch._current_hp/switch.max_hp)*100-oppDmg_onSwitch
            filler, switchScore = self.getMovesScore(switch, switchHpAfterSwitchIn, opp, [switch._moves[move] for move in switch._moves], battle, opp_max_hp, switchOutspeed, switchReliableRecovery, oppDmg_onSwitch, type_chart, -1)
            
            if switchScore > highestScore:
                highestScore = switchScore
                highestScoringPlay = switch
            print(f"{switch.species}.score \t= {switchScore:.2f}")
        '''end{score_available_switches}'''
        '''end{score_available_plays}'''
        print(f"Best play fount is {BattleOrder(highestScoringPlay)}")
        print("---------------------------------------------------------------------------------------------------")
        
        return BattleOrder(highestScoringPlay)
    
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

    def outspeed(self, myPokemon, oppPokemon):
        if myPokemon.base_stats["spe"] > oppPokemon.base_stats["spe"]:
            outspeed = 1
        else:
            outspeed = 0
        return outspeed
    
    def reliableRecovery(self, available_moves):
        for move in available_moves:
            if move._id == "softboiled" or move._id == "recover":
                reliableRecovery = 1
            else:
                reliableRecovery = 0
        return reliableRecovery
    
    def calculate_damage(self, level, attack_stat, defense_stat, base_power, stab, type_effectiveness):
        damage = (((2*level)/5+2)*base_power*attack_stat/defense_stat)/50+2
        damage *= stab
        damage *= type_effectiveness
        return int(damage)

    def get_opponent_strongest_move_damage(self, me, opp, battle):
        biggest_damage = 0
        if "SLP" in str(opp._status) or "FRZ" in str(opp._status):
            return biggest_damage
        type_chart = opp._data.type_chart
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
    
    def getMovesScore(self, myPokemon, currentHP_percentage, opp, available_moves, battle, opp_max_hp, outspeed, reliableRecovery, oppDmg, type_chart, highestScore):
        highestScoringPlay = None
        for move in available_moves:
            move_dmg = 0
            recoil = 0
            sideEffectVal = 0
            move_info = battle.available_moves[0]._moves_dict[move._id]
            acc = move_info["accuracy"]
            if move_info["secondary"] is not None:
                effectChance = move_info["secondary"]["chance"]/100
            else:
                effectChance = 1
            if move._id == "softboiled" or move._id == "recover" or move._id == "rest":
                #placeholder
                moveScore = -1
            elif move._id == "amnesia" or move._id == "reflect" or move._id == "agility":
                #placeholder
                moveScore = -1
            elif move._id == "counter" or move._id == "substitute":
                #placeholder
                moveScore = -1
            elif move._id == "explosion" or move._id == "selfdestruct":
                #placeholder
                moveScore = -1
            elif move._id == "seismictoss" or move._id == "nightshade":
                move_dmg = 100/opp_max_hp*100
                score_baseline = (currentHP_percentage-oppDmg)/100*(move_dmg)*(acc/100)/(oppDmg+1)
                if reliableRecovery == 1 and "SLP" not in str(opp._status) and "FRZ" not in str(opp._status):
                    score_baseline *= 50/(oppDmg+1)
                if move_dmg > opp._current_hp:
                    outspeed_benefit = outspeed*MAX_WEIGHT
                else:
                    outspeed_benefit = 0
                
                moveScore = score_baseline+outspeed_benefit
            else:
                category = move_info["category"]
                if category == "Status":
                    move_dmg = 0
                else:
                    if category == "Physical":
                        attack_stat = floor((myPokemon.base_stats["atk"]+15)*2+252/4)+5
                        defense_stat = floor((opp.base_stats["def"]+15)*2+252/4)+5
                        
                    else:
                        attack_stat = floor((myPokemon.base_stats["spa"]+15)*2+252/4)+5
                        defense_stat = floor((opp.base_stats["spd"]+15)*2+252/4)+5
                    move_type = move_info["type"].upper()
                    if move_type == myPokemon._type_1:
                        stab = 1.5
                    elif myPokemon._type_2 is not None and move_type == myPokemon._type_2:
                        stab = 1.5
                    else:
                        stab = 1
                    type_effectiveness = type_chart[opp._type_1.name.upper()][move_type]
                    if opp._type_2 is not None:
                        type_effectiveness *= type_chart[opp._type_2.name.upper()][move_type]
                    move_dmg = self.calculate_damage(100, attack_stat, defense_stat, move_info["basePower"], stab, type_effectiveness)
                    if move._id == "doubleedge":
                        recoil = (move_dmg/4)/myPokemon.max_hp*100
                    move_dmg = move_dmg/opp_max_hp*100

                if opp._status is None:
                    if move._id in sideEffects["FRZ"]:
                        sideEffectVal = 100*effectChance
                        for pokemon in battle.opponent_team.values():
                            if "FRZ" in str(pokemon._status):
                                sideEffectVal = 0
                    elif move._id in sideEffects["SLP"]:
                        sideEffectVal = 90*effectChance
                        for pokemon in battle.opponent_team.values():
                            if "SLP" in str(pokemon._status):
                                sideEffectVal = 0
                    elif move._id in sideEffects["PAR"]:
                        sideEffectVal = 50*effectChance
                    elif move._id in sideEffects["BRN"] or move._id in sideEffects["PSN"]:
                        sideEffectVal = 20*effectChance

                if move._id == "hyperbeam" and move_dmg < opp._current_hp:
                    moveScore = -1
                else:
                    score_baseline = (currentHP_percentage-oppDmg)/100*(move_dmg+sideEffectVal)*(acc/100)/(oppDmg+recoil+1)
                    if reliableRecovery == 1 and "SLP" not in str(opp._status) and "FRZ" not in str(opp._status):
                        score_baseline *= 50/(oppDmg+1)
                    if move_dmg > opp._current_hp:
                        outspeed_benefit = outspeed*MAX_WEIGHT
                    else:
                        outspeed_benefit = 0
                    moveScore = score_baseline+outspeed_benefit

            if moveScore > highestScore:
                highestScore = moveScore
                highestScoringPlay = move
            
            print(f"{move._id}.damage \t= {move_dmg:.2f}\t{move._id}.sideEff \t= {sideEffectVal:.2f}\t{move._id}.score  \t= {moveScore:.2f}")
        
        return highestScoringPlay, highestScore
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def print_Weak_Resis_Immun(self, battle, typeMatchup):
        print("Opponent [" + str(battle.opponent_active_pokemon.species) +"] is: ")
        print("Weak against -> " + str(typeMatchup[0]))
        print("Resistant against -> " + str(typeMatchup[1]))
        print("Immune against -> " + str(typeMatchup[2]) + "\n")