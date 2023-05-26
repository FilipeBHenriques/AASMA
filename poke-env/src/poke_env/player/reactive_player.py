"""This module defines a random players baseline
"""

from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder


class ReactivePlayer(Player):
    def choose_move(self, battle) -> BattleOrder:
        return self.choose_reactive_move(battle)
