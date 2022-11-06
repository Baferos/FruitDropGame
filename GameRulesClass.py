from GameParameters import startingLives, startSpeed


class GameRules:

    def __init__(self):
        self.score = 0
        self.lives = startingLives
        self.speed = startSpeed

    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def get_speed(self):
        return self.speed

    def set_score(self, score):
        self.score = score

    def set_lives(self, lives):
        self.lives = lives

    def set_speed(self, speed):
        self.speed = speed

    def add_speed(self, speed):
        self.speed += speed

    def increase_score(self):
        self.score += 1

    def increase_lives(self):
        self.lives += 1

    def decrease_lives(self):
        self.lives -= 1

    def reset(self):
        self.score = 0
        self.lives = startingLives
        self.speed = startSpeed

    def check_if_game_over(self):
        return self.lives <= 0

