import enum
# from abc import ABC, abstractmethod
from typing import Self

class WarehouseObject:
    direction_dict: dict[str,list[int]] = {
        '<': [-1, 0],
        '>': [1, 0],
        '^': [0, -1],
        'v': [0, 1],
    }
    
    def __init__(self, x: int, y: int, objects: list[list[Self]], map_cols: int, map_rows: int):
        self.x = x
        self.y = y
        self.objects = objects
        self.map_rows = map_rows
        self.map_cols = map_cols
        
        pass
    
    def __str__(self):
        raise NotImplementedError()
    
class MovableObject(WarehouseObject):
    
    def __init__(self, x: int, y: int, objects: list[list[WarehouseObject]], map_cols: int, map_rows: int):
        super().__init__(x, y, objects, map_cols, map_rows)
        self.objects: list[list[WarehouseObject]] = objects

    def move(self, direction: str) -> bool:
        translation = self.direction_dict[direction]
        new_x, new_y = self.x + translation[0], self.y + translation[1]
        
        if not(0 <= new_x < self.map_cols and 0 <= new_y < self.map_rows):
            return False
        
        dest_obj: WarehouseObject = self.objects[new_y][new_x]
        
        if isinstance(dest_obj, Air):
            self.objects[self.y][self.x], self.objects[new_y][new_x] = self.objects[new_y][new_x], self.objects[self.y][self.x]
            self.x += translation[0]
            self.y += translation[1]
            return True
        elif isinstance(dest_obj, Obstacle):
            return False
        elif isinstance(dest_obj, Box):
            if dest_obj.move(direction):
                self.objects[self.y][self.x], self.objects[new_y][new_x] = self.objects[new_y][new_x], self.objects[self.y][self.x]
                self.x += translation[0]
                self.y += translation[1]
                return True
            else:
                return False
        
    
class Obstacle(WarehouseObject):
    def __str__(self):
        return '#'

class Air(WarehouseObject):
    def __str__(self):
        return '.'

class Box(MovableObject):
    def __init__(self, x: int, y: int, objects: list[list[WarehouseObject]], map_cols: int, map_rows: int):
        super().__init__(x, y, objects, map_cols, map_rows)
        self.objects: list[list[WarehouseObject]] = objects
            
    def __str__(self):
        return 'O'

class Robot(MovableObject):
    
    def __init__(self, x: int, y: int, objects: list[list[WarehouseObject]], map_cols: int, map_rows: int):
        super().__init__(x, y, objects, map_cols, map_rows)
        self.objects: list[list[WarehouseObject]] = objects
        
    
    def __str__(self):
        return '@'
    
class Warehouse:
    def __init__(self, filepath: str):
        self.objects: list[list[WarehouseObject]] = []
        self.map_rows = 0
        self.map_cols = 0
        self.robot: Robot = None
        self.directions: str = None
        self.direction_index = 0
        
        with open('input.txt', 'r') as file:
            filedata = file.read().split('\n\n')
            map = filedata[0].split('\n')
            self.directions = filedata[1].replace('\n', '')
            self.map_rows = len(map)
            self.map_cols = len(map[0])
            
            for row in range(self.map_rows):
                self.objects.append([])
                for col in range(self.map_cols):
                    map_ch = map[row][col]
                    if map_ch == '#':
                        self.objects[row].append(Obstacle(col, row, self.objects, self.map_cols, self.map_rows))
                    elif map_ch == 'O':
                        self.objects[row].append(Box(col, row, self.objects, self.map_cols, self.map_rows))
                    elif map_ch == '.':
                        self.objects[row].append(Air(col, row, self.objects, self.map_cols, self.map_rows))
                    elif map_ch == '@':
                        self.objects[row].append(Robot(col, row, self.objects, self.map_cols, self.map_rows))
                        self.robot = self.objects[row][-1]
                        
    def update(self) -> bool:
        if self.direction_index < len(self.directions):
            self.robot.move(self.directions[self.direction_index])
            self.direction_index += 1
            return True
        else:
            return False
                
    def get_object(self, x: int, y: int) -> WarehouseObject:
        return self.objects[y][x]
    
    def calc_solution(self) -> int:
        sum = 0
        for x in range(self.map_cols):
            for y in range(self.map_rows):
                obj = self.get_object(x, y)
                if isinstance(obj, Box):
                    sum += x + y * 100
        return sum
    
    def __str__(self) -> str:
        output = []
        for row in range(self.map_rows):
            output.append(''.join([str(obj) for obj in self.objects[row]]))
        return '\n'.join(output)
                        

warehouse = Warehouse('input.txt')
print(warehouse)

while warehouse.update():
    pass
print(warehouse)

print(warehouse.calc_solution())


# print(warehouse)