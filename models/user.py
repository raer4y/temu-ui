'''
Model data User untuk mempresentasikan penggua civitas akademika UI
'''

class User:
    def __init__(self, username: str, password_hash: str, name: str, faculty: str, karma_points: int=0):
        self.username=username
        self.password_hash=password_hash
        self.name=name
        self.faculty=faculty
        self.karma_points=karma_points

    def add_karma(self, points: int):
        if points<0:
            raise ValueError('Poin karma tidak boleh negatif!')
        else:
            self.karma_points+=points

    def to_dict(self):
        return{
            'username': self.username,
            'password_hash': self.password_hash,
            'name': self.name,
            'faculty': self.faculty,
            'karma_points': self.karma_points
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username=data['username'],
            password_hash=data['password_hash'],
            name=data['name'],
            faculty=data['faculty'],
            karma_points=data.get('karma_points',0)
        )