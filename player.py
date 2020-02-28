class Player:
    def __init__(self):
        self.current_room = None # Input current room request in here. Status request finding room id or something
    def travel(self, direction):
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
        else:
            print("You cannot move in that direction.")
        # Replace with travel function using move request from API