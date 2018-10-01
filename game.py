class Game:
    def __init__(self, owner_id, name=None, min_person=None, max_person=None, place=None):
        self.owner_id = owner_id
        self.name = name
        self.min_person = min_person
        self.max_person = max_person
        self.place = place