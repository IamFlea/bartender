from aoc_object_clist import *

def int_to_str(number, allow_zero=True):
    if number == 0:
        return "0" if allow_zero else ""
    tostr = lambda x: str(int(x))
    if number < 1:
        # Get tenths 
        tenths = tostr(number*10)
        return "." + tenths 
    if number >= 10000:
        number /= 1000
        return tostr(number) + "k"
    elif number >= 1000:
        number2 = (number%1000)/100
        number /= 1000
        return tostr(number) + "." + tostr(number2)+ "k"
    return tostr(number)

def get_attack(obj, type=["4 - Base Melee"]):
    attack_type = Attack.BONUS_CLASS.index(type)
    for type, amount in obj.udata.attack:
        if attack_type in type:
            return amount
    return 0

def get_armor(obj, type=["4 - Base Melee"]):
    armor_type = Armor.BONUS_CLASS.index(type)
    for type, amount in obj.udata.armor:
        if armor_type == type:
            return amount
    return 0
    
def get_pierce_armor(obj, type=["3 - Base Pierce"]):
    armor_type = Armor.BONUS_CLASS.index(type)
    for type, amount in obj.udata.armor:
        if armor_type == type:
            return amount
    return 0
            
def get_armors(obj):
    return str(get_armor(obj)) + "/" + str(get_pierce_armor(obj))

def get_res_type_from_list(obj_list):
    for o in obj_list:
        if o.resource_type:
            return o.resource_type[0]
        