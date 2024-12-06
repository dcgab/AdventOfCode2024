import copy
from enum import Enum

# Enum for storing directions of the guard
class Direction(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Guard:
    _direction_translation_table = {
        Direction.TOP: [0, -1],
        Direction.RIGHT: [1, 0],
        Direction.BOTTOM:  [0, 1],
        Direction.LEFT: [-1, 0]
    }

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.direction = Direction.TOP

    def get_next_pos(self):
        # Get next position based on the direction
        rel_translation = self._direction_translation_table[self.direction]
        return [self.x + rel_translation[0], self.y + rel_translation[1]]
    
    def step(self) -> None:
        # Move the guard's position based on the direction
        next_pos = self.get_next_pos()
        self.x = next_pos[0]
        self.y = next_pos[1]

    def turn(self) -> None:
        # Turn 90 degrees clockwise
        self.direction = Direction((self.direction.value + 1) % 4)

class GuardMap:
    def __init__(self, map_path: str, obstruction_x: int = None, obstruction_y: int = None):
        with open(map_path, 'r') as file:
            self.map = [line.strip() for line in file.readlines()]

        # Initialize map with an obstruction
        if obstruction_x is not None and obstruction_y is not None:
            self.map[obstruction_y] = self.map[obstruction_y][:obstruction_x] + '#' + self.map[obstruction_y][obstruction_x+1:]

        # Keep track of previously visited guard positions
        self.visited_map = self.map.copy()
        self.rows = len(self.map)
        self.cols = len(self.map[0])

        # Find the guard's initial position and remove the marker
        for y in range(self.rows):
            for x in range(self.cols):
                if self.map[y][x] == '^':
                    self.guard = Guard(x, y)
                    self.map[y] = self.map[y].replace('^','.')

    # Calculate the coordinates from the guard until but not including the next object
    def get_guard_line_of_sight(self):
        sight_coords = []
        local_guard = copy.deepcopy(self.guard)
        sight_coords.append([local_guard.x, local_guard.y])
        while True:
            next_guard_pos = local_guard.get_next_pos()
            if not self.get_map_object(next_guard_pos[0], next_guard_pos[1]) == '#':
                local_guard.step()
                sight_coords.append([local_guard.x, local_guard.y])
            else:
                break
        return sight_coords

        
    def get_map_object(self, x: int, y: int) -> str:
        return self.map[y][x]
    
    def print_visited_map(self):
        for y in range(self.rows):
            print(self.visited_map[y])

    def update(self):
        # Update the visited map markers
        self.visited_map[self.guard.y] = self.visited_map[self.guard.y][:self.guard.x] + 'X' + self.visited_map[self.guard.y][self.guard.x+1:]
        next_guard_pos = self.guard.get_next_pos()

        # Check bounds
        if not(0 <= next_guard_pos[0] < self.cols and 0 <= next_guard_pos[1] < self.rows):
            return False

        # Turn if guard about to collide with an object
        if self.get_map_object(next_guard_pos[0], next_guard_pos[1]) == '#':
            self.guard.turn()
        else:
            self.guard.step()

        return True

# Since this object contains the map, keep an instance to reference to the parsed map
initialMap = GuardMap('input.txt', None, None)
line_of_sight = initialMap.get_guard_line_of_sight()

n_looping_obstructions = 0
for x in range(initialMap.cols):
    for y in range(initialMap.rows):
        # Prevent obstruction from being place at the guards location
        if x == initialMap.guard.x and y == initialMap.guard.y:
            continue

        # The number of unique visited guard positions
        unique_guard_pos_count = 1
        # The total amount of steps taken. Used to detect looping
        guard_pos_count = 1
        guardMap = GuardMap('input.txt', x, y)

        # Do not place obstructions within the line of sight
        if x == line_of_sight[0] and y == line_of_sight[1]:
            continue

        while guardMap.update():
            # Since the visited_map is marked for previous positions, we can check if next position is already visited
            if guardMap.visited_map[guardMap.guard.y][guardMap.guard.x] != 'X':
                unique_guard_pos_count += 1
            guard_pos_count += 1

            # Use a threshold of 10000 when detecting a loop
            if guard_pos_count > 10000:
                n_looping_obstructions += 1
                break
    # Print progress
    print(f"{(guardMap.rows * x + y) / (guardMap.cols * guardMap.rows) * 100:0.2f}%")

print('Obstructions:')
print(n_looping_obstructions)