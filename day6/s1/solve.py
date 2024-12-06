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
    def __init__(self, map_path: str):
        with open(map_path, 'r') as file:
            self.map = [line.strip() for line in file.readlines()]
        # Keep track of previously visited guard positions
        self.visited_map = self.map.copy()
        self.rows = len(self.map)
        self.cols = len(self.map[0])

        # Find the guard's initial position and remove the markerk
        for y in range(self.rows):
            for x in range(self.cols):
                if self.map[y][x] == '^':
                    self.guard = Guard(x, y)
                    self.map[y] = self.map[y].replace('^','.')

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
        self.guard.step()

        return True

# Guard position counter. Start with 1 for starting location
guard_pos_count = 1
guardMap = GuardMap('input.txt')
while guardMap.update():
    # Since the visited_map is marked for previous positions, we can check if next position is already visited
    if guardMap.visited_map[guardMap.guard.y][guardMap.guard.x] != 'X':
        guard_pos_count += 1

print(guard_pos_count)