import time,readline,thread
import sys,struct,fcntl,termios

def blank_current_readline():
    # Next line said to be reasonably portable for various Unixes
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    # ANSI escape sequences (All VT100 except ESC[0G)
    sys.stdout.write('\x1b[2K')                         # Clear current line
    sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
    sys.stdout.write('\x1b[0G')                         # Move to start of line

def safe_print(val):
    blank_current_readline()
    print val
    sys.stdout.write('> ' + readline.get_line_buffer())
    sys.stdout.flush()          # Needed or text doesn't show until a key is pressed
