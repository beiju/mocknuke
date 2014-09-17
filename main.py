import bluetooth
import field
from safe_print import safe_print

funcs = dict()

ignore_heartbeats = False

def handle_pkt(pkt):
    if not ignore_heartbeats or pkt.type != bluetooth.PacketType.heartbeat:
        safe_print(pkt)

def connect(inp=[]):
    if bluetooth.serial_port.isOpen():
        safe_print("Bluetooth is already connected.")
    else:
            
        if len(inp) == 0:
            which = None
        else:
            which = inp[0]
            
        bluetooth.start(which, handle_pkt, safe_print)
        
def ignore_heartbeats(inp=[]):
    global ignore_heartbeats
    try:
        ignore_heartbeats = ("yes" in inp[0]) or ("on" in inp[0])
    except IndexError:
        ignore_heartbeats = not ignore_heartbeats
    
    safe_print("Ignoring heartbeats: %r" % ignore_heartbeats)
        
funcs['connect'] = funcs['c'] = connect    
funcs['supply'] = field.supply
funcs['storage'] = field.storage
funcs['stop'] = field.stop
funcs['resume'] = funcs['res'] = field.resume
funcs['ignorehb'] = funcs["ignore_hb"] = funcs["ihb"] = ignore_heartbeats

def main():
    funcs['connect']()
    
    while True:
        try:
            inp = raw_input("> ").split()
            cmd = inp[0]
            inp = inp[1:] # input remaining after command
            
            if cmd == "exit":
                break
            elif cmd in funcs:
                funcs[cmd](inp)
            else:
                safe_print("! Unknown command `" + cmd + "`. Inputs: " + repr(inp)) 
            
        # Makes Ctrl-C clear the input like I'm used to from bash/zsh
        except KeyboardInterrupt:
            print #newline
            continue

if __name__ == "__main__":
    main()
