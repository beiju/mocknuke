from safe_print import safe_print
from bluetooth import PacketType, Packet

# Field state
# Bitmasks represented as lists for easier programming
availability = {
    "Supply": [True, True, True, True],
    "Storage": [False, False, False, False]
}

def tubenum(inp):
    """Returns the tube number or -1 for invalid input"""
    try:
        num = int(inp)
    except ValueError:
        return -1
    
    if num >= 0  and num < 4:
        return num
    else:
        return -1
        
def boolstr_to_list(str):
    return map(lambda val: val == '1', list(str))

def list_to_boolstr(list):
    return "".join(map(lambda val: '1' if val else '0', list))

def list_to_int(list):
    return reduce(lambda bits, bit: (bits << 1) | bit, list)

def avail(which, inp):
    global availability
    
    old_val = availability[which]
    if inp[0] == '+' or inp[0] == '-': 
        # If first character of first input is +, use +n notation to mark tube n as occupied
        num = tubenum(inp[1:]) # Get the tubenum with chars 1 through end of the first input
        if num == -1:
            safe_print("! "+which+" availability invalid, one number between 0 and 3 expected with +n or -n notation")
            return
        else:
            availability[which][num] = (inp[0] == '+')
    else:
        # Using bitmask mode
        if len(inp) != 4:
            safe_print("! "+which+" availability invalid, one 4-digit bitmask expected in bitmask mode")
            return
        else:
            for ch in inp:
                if ch != '0' and ch != '1':
                    print_safe("! "+which+" availability invalid, only 0 and 1 expected in bitmask mode")
                    return
            availability[which] = boolstr_to_list(inp)
            
    safe_print(which+" updated from 0b%s to 0b%s" % (list_to_boolstr(old_val), list_to_boolstr(availability[which])))
    
    typ = PacketType.supply_availability if which is 'Supply' else PacketType.storage_availability
    pkt = Packet(typ, list_to_int(availability[which]), destination=0)
    pkt.send()
    safe_print(pkt)

def supply(inp):
    if len(inp) != 1:
        safe_print("! Supply availability invalid, one argument expected")
        return
    else:
        avail("Supply", inp[0])
        
def storage(inp):
    if len(inp) != 1:
        safe_print("! Storage availability invalid, one argument expected")
        return
    else:
        avail("Storage", inp[0])
        
def stop(inp):
    try:
        pkt = Packet(PacketType.stop, destination=int(inp[0]))
    except (IndexError, ValueError):
        pkt = Packet(PacketType.stop)

    pkt.send()
    safe_print(pkt)
        
def resume(inp):
    pkt = Packet(PacketType.resume)
    pkt.send()
    safe_print(pkt)
