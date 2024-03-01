from a2_support import *
import math

# Implement your classes here


class Card:
    '''initial all the variable for class Card'''
    damage = 0
    block = 0
    energy = 1
    status = {}
    name = 'Card'
    description = 'A card.'
    target = True
    card = "Card()"
    
    
    def get_damage_amount(self) -> int:
        '''returns the amount of damage this card does to its target'''
        return self.damage
    
    def get_block(self) -> int:
        '''returns the amount of block this card adds to user'''
        return self.block

    def get_energy_cost(self) -> int:
        '''returns the amount of energy the card costs to play'''
        return self.energy

    def get_status_modifiers(self) -> dict[str, int]:
        '''returns a dic describing each status modifiers applied
        when this card is played returns default when no status applied
'''
        return self.status

    def get_name(self) -> str:
       '''returns the name of the card - Card'''
       return self.name
       
    
    def get_description(self) -> str:
        '''returns the description of the card'''
        return self.description

    def requires_target(self) -> bool:
        '''returns 1 if the card requires a target, if not return false''' 
        return self.target

        
    def __str__(self) -> str:
        '''return the represetntaion for the card:
            {Card name}: {Card description}'''
        return self.name + ": " + self.description

    def __repr__(self) -> str:
        '''returns the text that would be required to create a
        new iinstance of this class identical to self'''
        return (f"{self.__class__.__name__}()")
    
class Strike(Card):
    '''initial all variables for card - Strike'''
    damage = 6
    block = 0
    energy = 1
    name = "Strike"
    description = "Deal 6 damage."
    target = True


class Defend(Card):
    '''initial all variables for card - Defend'''
    damage = 0
    block = 5
    energy = 1
    name = "Defend"
    description = "Gain 5 block."
    target = False


class Bash(Card):
    '''initial all variables for card - Bash'''
    damage = 7
    block = 5
    energy = 2
    name = "Bash"
    description = "Deal 7 damage. Gain 5 block."
    target = True

class Neutralize(Card):
    '''initial all variables for card - Neutralize'''
    damage = 3
    block = 0
    energy = 0
    status = {'weak': 1, 'vulnerable': 2}
    name = "Neutralize"
    description = "Deal 3 damage. Apply 1 weak. Apply 2 vulnerable."


class Survivor(Card):
    '''initial all variables for card - Survivor'''
    damage = 0
    block = 8
    energy = 1
    status = {'strength': 1}
    target = False
    name = "Survivor"
    description = "Gain 8 block and 1 strength."


class Entity:
    '''class for all entity, returns status such as:
        hp, max_hp, weak, reduced hp, strength, vulnerable, block'''
    def __init__(self, max_hp: int) -> None:
        '''initial all the variables for entity'''
        self._max_hp = max_hp #maximum HP for entity
        self._hp = max_hp #current HP for entity
        self._block = 0
        self._strength = 0
        self._weak = 0
        self._vulnerable = 0
        self._injury = 0
        self._reduce_hp = 0
   
    def get_hp(self) -> int:
        '''returns the current HP of the entity'''
        return self._hp
    
    def get_max_hp(self) -> int:
        '''returns the maximum possible HP for this entity'''
        return self._max_hp

   
    def get_block(self) -> int:
        '''return the amount of block for this entity'''
        return self._block
    
    def get_strength(self) -> int:
        '''return the amount of strength for this entity'''
        return self._strength

        
    def get_weak(self) -> int:
        '''return the amount of weak for this entity'''
        return self._weak
       
    def get_vulnerable(self) -> int:
        '''return the number of turns for which this entity is vulnerable'''
        return self._vulnerable

    def get_name(self) -> int:
        '''returns the name of the entity.'''
        return self.__class__.__name__
    
    def reduce_hp(self, amount: int) -> None:
        '''attack entity with a damage of amount involves reducing block
            until damage has done or block has reduced to zero
            in which case the HP is reduced by remaining amount HP cannot <0'''
        self._reduce_hp += amount
        self._hp = self._hp + self._block - self._reduce_hp
        if self._hp <= 0:
            self._hp = 0
        else:
            return self._hp
                   
    def is_defeated(self) -> bool:
        '''detect if an entity is defeated by returning True or False'''
        if self._hp == 0:
            return True
        else:
            return 0

    def add_block(self, amount: int) -> None: 
        '''adds the amount of block entity has'''
        self._block += amount
    
    def add_vulnerable(self, amount: int) -> None:
        '''add the given amount to the amount of vulnerable this entity has'''
        self._vulnerable += amount

    def add_weak(self, amount: int) -> None:
        '''add the given amount to the amount of the weak this entity has'''
        self._weak += amount


    def add_strength(self, amount: int) -> None:
        '''adds the given amount to the amount of block this entity has'''
        self._strength += amount

    def new_turn(self) -> str:
        '''set up for new turn'''
        self._block = self._reduce_hp - self._block
        
        if self._block <= 0:
            self._block = 0
        else:
            return self._block
        
        if self._weak >= 1:
            self._weak = self._weak - 1
        else:
            return 0
        
        if self._vulnerable >= 1:
            self._vulnerable = self._vulnerable - 1
        else:
            return 0
        

    def __str__(self) -> str:
        '''return required str for each class'''
        return "{}: {}/{} HP".format(self.get_name(), self.get_hp(), self.get_max_hp()) 

    def __repr__(self) -> str:
        '''return required __repr__ for each class'''
        return "{}({})".format(self.get_name(), self.get_max_hp())
       
            
class Player(Entity):
    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        '''player energy starts at 3
            list of card: deck hand and discard pile'''
        super().__init__(max_hp)
        self._energy = 3
        self.cards = cards
        self.deck = self.cards
        self.hand = []
        self.discarded = []
        if self.cards == []:
            self.deck = []
        else:
            self.deck = cards

        
    def get_energy(self) -> int:
        '''return the amount of energy player have'''
        return self._energy

    def get_hand(self) -> list[Card]:
        '''return the list of hand'''
        return self.hand

    def get_deck(self) -> list[Card]:
        '''return list of deck'''
        return self.deck
    
    def get_discarded(self) -> list[Card]:
        '''return discard pile list'''
        return self.discarded

    def start_new_encounter(self) -> None:
        '''start a new turn, put card in discard pile to deck
            and empty card in hand'''
        self.deck.extend(self.discarded)
        self.discarded.clear()

    def end_turn(self) -> None:
        '''end of the turn, put card in hand to discard pile
            and empty card in hand'''
        self.discarded.extend(self.hand)
        self.hand.clear()

    def new_turn(self) -> None:
        '''inherit from new turn in entity, call for new turn
            give 3 energy for player to play card
            and draw cards using a2_support'''
        super().new_turn()
        self._energy = 3
        draw_cards(self.deck, self.hand, self.discarded)

        
    def play_card(self, card_name: str) -> Card | None:
        card_found: Card | None = None
        '''transfer all card in hand into str,
            and detect if the card applied match the card in hand,
            if all true, player play card and card goes to discard pile
             and lost one energy, '''
        for card in self.hand:
                for card_name in card.get_name():
                    if self._energy >= 1:
                        card_found = card
                    
                            
        self.hand.remove(card_found)
        self._energy - 1
        self.discarded.append(card_found)
        return card_found

    
    def __repr__(self) -> str:
        '''return in a format of name(max_hp, cards)'''
        return '{}({}, {})'.format(self.get_name(), self._max_hp, self.cards)

class IronClad(Player):
    '''inherit from player. Return the cards ironclad have, setup max-hp'''
    def __init__(self):
        '''inherit and initial all the variabless for the player IronClad'''
        self.cards = [Strike(),Strike(),Strike(),Strike(), Strike(),
                     Defend(), Defend(),Defend(),Defend(),
                     Bash()]
        super().__init__(80, self.cards)
        
    def __repr__(self) -> str:
        '''return __repr__ for IronClad()'''
        return self.get_name() + '()'
        

class Silent(Player):
    '''inherit from player, return cards silent have and set its max_hp'''
    def __init__(self):
        '''inherit and initial all the variabless for the player Silent'''
        self.cards = [Strike(),Strike(),Strike(),Strike(), Strike(),
                     Defend(), Defend(), Defend(),Defend(),Defend(),
                     Neutralize(),Survivor()]
        super().__init__(70, self.cards)
        
    def __repr__(self) -> str:
        '''return __repr__ for Silent()'''
        return self.get_name() + '()'

class Monster(Entity):
    '''provide all function required for monster, specifically:
        its damage to player(action), and return their id/name'''
    initial_id = 0
    def __init__(self, max_hp: int) -> None:
        '''give the maximum hp for the monster
            give the id/ name for the monster'''
        super().__init__(max_hp)
        self._id = int(Monster.initial_id)
        Monster.initial_id += 1

    def get_id(self) -> int:
        '''return the name of the monsters'''
        return self._id
    
    def action(self) -> dict[str, int]:
        '''return the actions of the monsters, this remain as NotImplementedError'''
        raise NotImplementedError

class Louse(Monster):
    '''inherit from monster, return all detail and action for monster Louse'''
    def __init__(self, max_hp: int) -> None:
        '''initial all the variables for monster-Louse'''
        super().__init__(max_hp)
        self._entity = 'Louse(10)'
        self._max_hp = 10 #maximum HP for entity
        self._hp = 10 #current HP for entity
        self._name = 'Louse'
        self.damage_amount = random_louse_amount()

    def action(self) -> dict[str, int]:
        '''imported from a2.support so Louse can have random damage amount
        from 5 - 7'''
        
        _action = {'damage': self.damage_amount}
        return _action
    
class Cultist(Monster):
    '''return all the required info for monster-cultist
        e.g. unique damage_amount it gives, unique weak_amount it gives'''
    
    def __init__(self, max_hp: int) -> None:
        '''initial all the variables for monster-Cultist'''
        super().__init__(max_hp)
        self.num_calls = 0
        self.damage_amount = 0
        self.weak_amount = 0


    def action(self) -> dict[str, int]:
        '''initial monster-Cultist's action,
        gradually increase in damage amount and alternative weak amount'''
        
        _action = {'damage': self.damage_amount, 'weak': self.weak_amount}
        if self.num_calls % 2 == 0:
            self.weak_amount = 1
        else:
            self.weak_amount = 0
        self.num_calls += 1
        self.damage_amount = 6 + self.num_calls    
        return _action

class JawWorm(Monster):
    '''return all the required info for monster-JawWorm
        e.g. unique damage_amount it gives, unique block_amount it gives'''
    
    def __init__(self, max_hp: int) -> None:
        '''initial all the variable for monster-JawWorm,
        careful with round up and round down for
        damage amount and block amount'''
        super().__init__(max_hp)
        self._block = 0
        self.taken_damage_amount = 0
        self.current_damage_amount = 0

    def action(self) -> dict[str, int]:
        '''calculation of JawWorm damage amount and block amount'''
        self._block += math.ceil(self.taken_damage_amount/2)
        self.current_damage_amount += math.floor(self.taken_damage_amount/2)
        _action = {'damage': self.current_damage_amount}
        return _action
        
    
    def reduce_hp(self, amount: int) -> None:
        '''JawWorm's taken damage amount equal
        to the difference between max hp and current hp'''
        super().reduce_hp(amount)
        self.taken_damage_amount = super().get_max_hp() - super().get_hp()
        
        

class Encounter:
    '''return all required function for encounter, deal with fight and turns'''
    def __init__(self, player: Player, monsters: list[tuple[str, int]]) -> None:
        '''initial monster's tuple, player. introduce all monsters
        let the initial of player's turn equal to false,
        player turn only starts when its called
        '''
        self._player = player
        self._monsters = monsters
        self._monsters: list[Monster] = []
        
        for monster in monsters:
            get_name = monster[0]
            get_max_hp = monster[1]
            if get_name == 'Louse':
                self._monsters.append(Louse(get_max_hp))
            elif get_name == 'Cultist':
                self._monsters.append(Cultist(get_max_hp))
            elif get_name == 'JawWorm':
                self._monsters.append(JawWorm(get_max_hp))
            else:
                return False       
        self._player_new_turn = True
        self._player.start_new_encounter()
    
    def start_new_turn(self) -> None:
        '''return True to starts player's new_turn and call to new turn'''
        self._player_new_turn = True
        self._player.new_turn()
            
    def end_player_turn(self) -> None:
        '''return False to end player's turn,call to end, start monster's turn'''
        self._player_new_turn = False
        self._player.end_turn()
        for item in self._monsters:
            item.new_turn()

    def get_player(self) -> Player:
        '''return the player in the encounter'''
        return self._player

    def get_monsters(self) -> list[Monster]:
        '''returns the monsters remaining in the encounter'''
        return self._monsters

    def is_active(self) -> bool:
        '''if the monster still exist in the list,
        player should keep fighting'''
        if len(self._monsters) == 0:
            return False
        else:
            return True

    def player_apply_card(self, card_name: str,
                          target_id: int | None = None) -> bool:
        '''detect if player is at player turn, if target id exist
        and if terget id is equal to existing monster id
        for any of the condition '''
        monster_id = Monster.get_id()
        if self._player_new_turn == False:
            return False
    
        if target_id != monster_id:
            return False
                 
        if target_id is None:
            return False

        '''if card not in the card or not successful,
        return false or continue'''
        card = self._player.play_card(card_name)
        if card == False:
            return False
        else:
            return True

        '''add block or strength to the player'''
        self._player.add_block()
        self._player.add_strength()

        '''if target was specified, apply any vulnerable and weak
            damage calculated and applied to target,
            damage(vulnerable + strength + weak + base damage)'''
        self._player_damage = 0
        if terget_id == monster_id:
            if self._player.get_vulnerable() >= 1:
                self._player_damage = self._player.get_vulnerable * 1.5
            else:
                return damage_amount
            
            if self._player.get_weak() >= 1:
                self._player_damage = self._player.get_vulnerable * 0.75
            else:
                return self.player_damage

            self._player_damage = self.player_damage + self._player.get_strength

        return self._player_damage

        

    def enemy_turn(self) -> None:
        '''add weak and vulnerable to the player if the monster have any
            detect -> add to player
            add strength to monster/enemy itself
            detect -> add to monster/enemy'''
        self.enemy_damage = 0
        for enemy in self._monsters:
            enemy_action = enemy._action()
            if 'weak' in enemy_action:
                self._player.add_weak(enemy_action['weak'])
            if 'vulnerable' in enemy_action():
                self._player.add_vulnerable(enemy_action['vulnerable'])
            if 'strength' in enemy_action():
                self._monsters.add_strength(enemy_action['strength'])

        for enemy in self._monsters:
            '''calculate the amount of damage(base_damage+strength) the monster gives'''
            if 'damage' in enemy_action():
                self.enemy_damage += enemy_action['damage']
                self.enemy_damage += enemy.get_strength()
            '''detect if player have vulnerable or monster have weak.
            if the turn remained for vulnerable and weak is larger than one
            then, apply effect'''
            if player.get_vulnerable() >= 1:
                int(self.enemy_damage * 1.5)
            
            if enemy.get_weak() >= 1:
                int(self.enemy_damage * 0.75)



def main():
    '''ask which character player would like to choose'''
    character = input("please select your character: IronClad or Silent")
    player_character = 0
    if character == 'IronClad':
        player_character = IronClad()
    elif character == 'Silent':
        player_character = Silent()
    else:
        print("This Character does not exist, please check and try again.")

    '''show player the details of the monster in current monster list'''
    print(read_game_file(Encounter.get_monsters(monsters)))
    
    
            
if __name__ == '__main__':
    main()
