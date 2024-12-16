import enum
# from abc import ABC, abstractmethod
from typing import Self

class ComponentPart(enum.Enum):
    LEFT = 0
    RIGHT = 1

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
    
class WareHouseObjectComponent:    
    def __init__(self, parent: WarehouseObject, component_part: ComponentPart):
        self.parent = parent
        self.component_part = component_part
        self.other = None
        
    def set_other(self, other: Self) -> None:
        self.other = other
        
    def get_coord(self) -> list[int]:
        x_offset = 1 if self.component_part == ComponentPart.RIGHT else 0
        return [self.parent.x + x_offset, self.parent.y]
    
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
        elif isinstance(dest_obj, BoxComponent):
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
    
# class ObstacleComponent(WareHouseObjectComponent):
#     def __init__(self, parent: Obstacle, component_part: ComponentPart):
#         super().__init__(parent, component_part)
        
#     def __str__(self):
#         return '#'

class Air(WarehouseObject):
    def __str__(self):
        return '.'

class Box(MovableObject):
    def __init__(self, x: int, y: int, objects: list[list[WarehouseObject]], map_cols: int, map_rows: int):
        super().__init__(x, y, objects, map_cols, map_rows)
        self.objects: list[list[WarehouseObject]] = objects
            
    def __str__(self):
        return 'O'
    
class BoxComponent(WareHouseObjectComponent):
    def __init__(self, parent: Box, component_part: ComponentPart):
        super().__init__(parent, component_part)
        
    def can_move_vertical(self, direction: str) -> bool:
        translation = self.parent.direction_dict[direction]
        current_coords = self.get_coord()
        other_coords = self.other.get_coord()
        new_current_x, new_current_y = current_coords[0] + translation[0], current_coords[1] + translation[1]
        new_other_x, new_other_y = other_coords[0] + translation[0], other_coords[1] + translation[1]
        
        # y-level is the same so we only have to check one coord
        if not(0 <= new_current_x < self.parent.map_cols and 0 <= new_current_y < self.parent.map_rows):
            return False
        
        current_dest_obj: WarehouseObject = self.parent.objects[new_current_y][new_current_x]
        other_dest_obj: WarehouseObject = self.parent.objects[new_other_y][new_other_x]
        
        # for dest_obj in [current_dest_obj, other_dest_obj]:
        if isinstance(current_dest_obj, Air) and isinstance(other_dest_obj, Air):
            return True
        elif isinstance(current_dest_obj, Obstacle) or isinstance(other_dest_obj, Obstacle):
            return False
        else:
            # One of objects is a box
            current_can_move = True
            other_can_move = True
            if isinstance(current_dest_obj, BoxComponent):
                current_can_move = current_dest_obj.can_move_vertical(direction)
            if isinstance(other_dest_obj, BoxComponent):
                other_can_move = other_dest_obj.can_move_vertical(direction)
                
            if current_can_move and other_can_move:
                return True
            else:
                return False
        
    def move(self, direction: str) -> bool:
        translation = self.parent.direction_dict[direction]
        if direction == '<' or direction == '>':
            current_coords = self.get_coord()
            other_coords = self.other.get_coord()
            new_x, new_y = other_coords[0] + translation[0], other_coords[1] + translation[1]
        
            if not(0 <= new_x < self.parent.map_cols and 0 <= new_y < self.parent.map_rows):
                return False
        
            dest_obj: WarehouseObject = self.parent.objects[new_y][new_x]
            
            if isinstance(dest_obj, Air):
                # Update coordinates on the object map
                self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_y][new_x] = self.parent.objects[new_y][new_x], self.parent.objects[other_coords[1]][other_coords[0]]
                self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[other_coords[1]][other_coords[0]] = self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[current_coords[1]][current_coords[0]]
                # Update actual coordinates of the boxother_coords
                self.parent.x += translation[0]
                self.parent.y += translation[1]
                return True
            elif isinstance(dest_obj, Obstacle):
                return False
            elif isinstance(dest_obj, BoxComponent):
                if dest_obj.move(direction):
                    # Update coordinates on the object map
                    self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_y][new_x] = self.parent.objects[new_y][new_x], self.parent.objects[other_coords[1]][other_coords[0]]
                    self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[other_coords[1]][other_coords[0]] = self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[current_coords[1]][current_coords[0]]
                    # Update actual coordinates of the box
                    self.parent.x += translation[0]
                    self.parent.y += translation[1]
                    return True
                else:
                    return False
        elif direction == '^' or direction == 'v':
            current_coords = self.get_coord()
            other_coords = self.other.get_coord()
            new_current_x, new_current_y = current_coords[0] + translation[0], current_coords[1] + translation[1]
            new_other_x, new_other_y = other_coords[0] + translation[0], other_coords[1] + translation[1]
            
            # y-level is the same so we only have to check one coord
            if not(0 <= new_current_x < self.parent.map_cols and 0 <= new_current_y < self.parent.map_rows):
                return False
            
            current_dest_obj: WarehouseObject = self.parent.objects[new_current_y][new_current_x]
            other_dest_obj: WarehouseObject = self.parent.objects[new_other_y][new_other_x]
            
            # for dest_obj in [current_dest_obj, other_dest_obj]:
            if isinstance(current_dest_obj, Air) and isinstance(other_dest_obj, Air):
                # Update coordinates on the object map
                self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[new_current_y][new_current_x] = self.parent.objects[new_current_y][new_current_x], self.parent.objects[current_coords[1]][current_coords[0]]
                self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_other_y][new_other_x] = self.parent.objects[new_other_y][new_other_x], self.parent.objects[other_coords[1]][other_coords[0]]
                # self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_y][new_x] = self.parent.objects[new_y][new_x], self.parent.objects[other_coords[1]][other_coords[0]]
                # self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[other_coords[1]][other_coords[0]] = self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[current_coords[1]][current_coords[0]]
                # # Update actual coordinates of the boxother_coords
                self.parent.x += translation[0]
                self.parent.y += translation[1]
                return True
            elif isinstance(current_dest_obj, Obstacle) or isinstance(other_dest_obj, Obstacle):
                return False
            else:
                current_can_move = True
                other_can_move = True
                if isinstance(current_dest_obj, BoxComponent):
                    current_can_move = current_dest_obj.can_move_vertical(direction)
                if isinstance(other_dest_obj, BoxComponent):
                    other_can_move = other_dest_obj.can_move_vertical(direction)
                    
                
                    
                if current_can_move and other_can_move:
                    
                    if isinstance(current_dest_obj, BoxComponent) and isinstance(other_dest_obj, BoxComponent):
                        if current_dest_obj.parent == other_dest_obj.parent:
                            current_dest_obj.move(direction)
                        else:
                            current_dest_obj.move(direction)
                            other_dest_obj.move(direction)
                    else:
                        if isinstance(current_dest_obj, BoxComponent):
                            current_dest_obj.move(direction)
                        if isinstance(other_dest_obj, BoxComponent):
                            other_dest_obj.move(direction)
                    # Update coordinates on the object map
                    self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[new_current_y][new_current_x] = self.parent.objects[new_current_y][new_current_x], self.parent.objects[current_coords[1]][current_coords[0]]
                    self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_other_y][new_other_x] = self.parent.objects[new_other_y][new_other_x], self.parent.objects[other_coords[1]][other_coords[0]]
                    # # Update actual coordinates of the box
                    self.parent.x += translation[0]
                    self.parent.y += translation[1]
                    return True
                else:
                    return False
                    
            # elif (isinstance(current_dest_obj, BoxComponent) and isinstance(other_dest_obj, BoxComponent)):
            #     # Since we move two boxes, we need to check all 'paths' without actually moving in case it is not possible
            #     if current_dest_obj.can_move_vertical(direction) and other_dest_obj.can_move_vertical(direction):
            #         current_dest_obj.move(direction)
            #         other_dest_obj.move(direction)
            #         # Update coordinates on the object map
            #         self.parent.objects[current_coords[1]][current_coords[0]], self.parent.objects[new_current_y][new_current_x] = self.parent.objects[new_current_y][new_current_x], self.parent.objects[current_coords[1]][current_coords[0]]
            #         self.parent.objects[other_coords[1]][other_coords[0]], self.parent.objects[new_other_y][new_other_x] = self.parent.objects[new_other_y][new_other_x], self.parent.objects[other_coords[1]][other_coords[0]]
            #         # # Update actual coordinates of the box
            #         self.parent.x += translation[0]
            #         self.parent.y += translation[1]
            #         return True
            #     else:
            #         return False
                
            
        # translation = self.direction_dict[direction]
        # new_x, new_y = self.x + translation[0], self.y + translation[1]
        
        # if not(0 <= new_x < self.map_cols and 0 <= new_y < self.map_rows):
        #     return False
        
        # dest_obj: WarehouseObject = self.objects[new_y][new_x]
        
        # if isinstance(dest_obj, Air):
        #     self.objects[self.y][self.x], self.objects[new_y][new_x] = self.objects[new_y][new_x], self.objects[self.y][self.x]
        #     self.x += translation[0]
        #     self.y += translation[1]
        #     return True
        # elif isinstance(dest_obj, Obstacle):
        #     return False
        # elif isinstance(dest_obj, BoxComponent):
        #     if dest_obj.move(direction):
        #         self.objects[self.y][self.x], self.objects[new_y][new_x] = self.objects[new_y][new_x], self.objects[self.y][self.x]
        #         self.x += translation[0]
        #         self.y += translation[1]
        #         return True
        #     else:
        #         return False
        
    def __str__(self):
        if self.component_part == ComponentPart.LEFT:
            return '['
        else:
            return ']'

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
            self.map_cols = len(map[0]) * 2
            
            for row in range(len(map)):
                self.objects.append([])
                for col in range(len(map[0])):
                    map_ch = map[row][col]
                    if map_ch == '#':
                        self.objects[row].append(Obstacle(col*2, row, self.objects, self.map_cols, self.map_rows))
                        self.objects[row].append(Obstacle(col*2+1, row, self.objects, self.map_cols, self.map_rows))
                    elif map_ch == 'O':
                        box = Box(col*2, row, self.objects, self.map_cols, self.map_rows)
                        left_box = BoxComponent(box, ComponentPart.LEFT)
                        right_box = BoxComponent(box, ComponentPart.RIGHT)
                        left_box.set_other(right_box)
                        right_box.set_other(left_box)
                        self.objects[row].append(left_box)
                        self.objects[row].append(right_box)
                    elif map_ch == '.':
                        self.objects[row].append(Air(col*2, row, self.objects, self.map_cols, self.map_rows))
                        self.objects[row].append(Air(col*2+1, row, self.objects, self.map_cols, self.map_rows))
                    elif map_ch == '@':
                        self.objects[row].append(Robot(col*2, row, self.objects, self.map_cols, self.map_rows))
                        self.robot = self.objects[row][-1]
                        self.objects[row].append(Air(col*2+1, row, self.objects, self.map_cols, self.map_rows))
                        
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
                if isinstance(obj, BoxComponent) and obj.component_part == ComponentPart.LEFT:
                    sum += x + y * 100
        return sum
    
    def __str__(self) -> str:
        output = []
        for row in range(self.map_rows):
            # print(self.objects[row])
            output.append(''.join([str(obj) for obj in self.objects[row]]))
        return '\n'.join(output)
                        

warehouse = Warehouse('input.txt')
print(warehouse)

while warehouse.update():
    pass
    # print(f'move: {warehouse.directions[warehouse.direction_index]}')
print(warehouse)

# print(warehouse.calc_solution())


print(warehouse.calc_solution())