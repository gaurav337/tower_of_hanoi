import time
import os
import sys

NUM_DISKS = 5
DELAY_BETWEEN_MOVES = 0.5
INITIAL_PAUSE = 1.5

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def create_initial_pegs():
    pegs = {
        0: list(range(NUM_DISKS, 0, -1)),
        1: [],
        2: []
    }
    return pegs
# RECURSION breaking N-disk problem into two N-1 subproblems
def generate_moves(n, source, destination, auxiliary, move_list):
    if n == 0:
        return

    generate_moves(n - 1, source, auxiliary, destination, move_list)

    move_list.append((source, destination))

    generate_moves(n - 1, auxiliary, destination, source, move_list)

def render_disk(disk_size):
    blocks = "█" * (disk_size * 2 - 1)
    formatted = "[" + blocks + "]"
    return formatted

def render_empty_pole():
    return "|"

def render_frame(pegs):
    clear_screen()
    column_width = NUM_DISKS * 2 + 3
    total_height = NUM_DISKS + 2

    for row in range(total_height, 0, -1):

        line = "    "

        for peg_index in range(3):

            stack = pegs[peg_index]

            if row <= len(stack):
                disk_size = stack[row - 1]
                disk_str = render_disk(disk_size)
                padded = disk_str.center(column_width)
            else:
                pole_str = render_empty_pole()
                padded = pole_str.center(column_width)

            line += padded + "  "

        print(line)

    floor_line = "    "
    for peg_index in range(3):
        floor_segment = "═" * column_width
        floor_line += floor_segment + "  "
    print(floor_line)

    label_line = "    "
    peg_names = ["Peg A", "Peg B", "Peg C"]
    for peg_index in range(3):
        label = peg_names[peg_index].center(column_width)
        label_line += label + "  "
    print(label_line)

    print()

def execute_move(pegs, source, destination):
    disk = pegs[source].pop()
    pegs[destination].append(disk)
    return disk

def display_move_info(move_number, total_moves, disk, source, destination):
    peg_names = {0: "A", 1: "B", 2: "C"}

    print(
        f"    Move {move_number} of {total_moves}:  "
        f"Disk {disk}  ──►  "
        f"Peg {peg_names[source]} to Peg {peg_names[destination]}"
    )

def display_intro(total_moves):
    print(
        f"    Solving with {NUM_DISKS} disks  │  "
        f"{total_moves} moves required  │  "
        f"Minimum = 2^{NUM_DISKS} - 1 = {2**NUM_DISKS - 1}"
    )
    print()

def display_completion():
    print("    ✓  All disks successfully transferred!")
    print()

def run():

    pegs = create_initial_pegs()

    move_list = []
    generate_moves(NUM_DISKS, 0, 2, 1, move_list)
    total_moves = len(move_list)

    render_frame(pegs)
    display_intro(total_moves)

    print("    Press Enter to begin...")
    input()
    
    # Iterates through the generated moves and executes them
    for move_number, (source, destination) in enumerate(move_list, start=1):

        disk = execute_move(pegs, source, destination)

        render_frame(pegs)
        display_move_info(move_number, total_moves, disk, source, destination)

        time.sleep(DELAY_BETWEEN_MOVES)

    print()
    display_completion()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\n    Interrupted.\n")
        sys.exit(0)