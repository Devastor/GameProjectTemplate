





from abc import ABC, abstractmethod
from tkinter import *
import random
import time

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
GAME_WIDTH = 400
GAME_HEIGHT = 500

SCORE_X = 450
SCORE_Y = 50

PLAYER_START_X = 100
PLAYER_START_Y = 100
PLAYER_SIZE = 30
PLAYER_STEP = 1

ENEMY_START_X = 300
ENEMY_START_Y = 200
ENEMY_SIZE = 40
ENEMY_STEP = 10

BULLET_SIZE = 10
BULLET_STEP = 5
BULLET_INTERVAL = 1000

class GameManager:

    def __init__(self, windows = 0, worlds = 0, scoreBoards = 0, players = 0, enemies = 0):
        self._idCount = 0
        self.windows = windows
        self.worlds = worlds
        self.scoreBoards = scoreBoards
        self.players = players
        self.enemies = enemies
        self.bullets = []

        if (self.windows): self.createWindow()
        if (self.worlds): self.createWorld()
        if (self.scoreBoards): self.createScoreBoard()
        if (self.players): self.createPlayer()
        if (self.enemies): self.createEnemy()

    def draw(self):
        if (self.windows): self.drawWindow()
        if (self.worlds): self.drawWorld()
        if (self.enemies): self.drawEnemies()
        if (self.players): self.drawPlayers()
        if (self.scoreBoards): self.drawScoreBoard()

    def __del__(self):
        self.deletePlayer(self._player.getId())
        self.deleteEnemie(self._enemy.getId())
        self.deleteScoreBoard(self._sb.getId())
        self.deleteWorld(self._wrld.getId())
        self.deleteWindow(self.gw.getId())

    def getNewId(self):
        self._idCount += 1
        return self._idCount

    # creation part
    def createWindow(self):
        self.gw = GameWindow(self.getNewId())
        self.gw.create(0, 0)

    def createWorld(self):
        self._wrld = GameWorld(self.getNewId())

    def createPlayer(self):
        self._player = Player(self.getNewId(), PLAYER_START_X, PLAYER_START_Y)

    def createEnemy(self):
        self._enemy = Enemy(self.getNewId(), ENEMY_START_X, ENEMY_START_Y)

    def createScoreBoard(self):
        self._sb = ScoreBoard(self.getNewId(), SCORE_X, SCORE_Y)

    def createBullet(self, x, y):
        bullet = Bullet(self.getNewId(), x, y)
        self.bullets.append(bullet)

    # drawing part
    def drawWindow(self):
        self.gw.draw(0, 0)

    def drawWorld(self):
        pass

    def drawPlayers(self):
        self._player.draw(PLAYER_START_X, PLAYER_START_Y)

    def drawEnemies(self):
        self._enemy.draw(ENEMY_START_X, ENEMY_START_Y)

    def drawScoreBoard(self):
        self._sb.draw(SCORE_X, SCORE_Y)

    # deletion part
    def deleteWindow(self, id):
        pass

    def deleteWorld(self, id):
        pass

    def deletePlayer(self, id):
        pass

    def deleteEnemie(self, id):
        pass

    def deleteScoreBoard(self, id):
        pass

    def deleteBullet(self, id):
        for bul in self.bullets:
            if bul.getId() == id:
                self.bullets.remove(bul)
                self._idCount -= 1
                break

    def getEnemy(self):
        return self._enemy

    def getPlayer(self):
        return self._player


class GameObject(ABC):

    def __init__(self, id):
        self._id = id

    @abstractmethod
    def create(self, x, y):
        pass

    @abstractmethod
    def draw(self, x, y):
        pass

    @abstractmethod
    def delete(self):
        pass

    @property
    @abstractmethod
    def getId(self):
        pass

class Entity(ABC):

    @property
    @abstractmethod
    def getX(self):
        pass

    @property
    @abstractmethod
    def getY(self):
        pass

    @abstractmethod
    def move(self, direction, step):
        pass

    @abstractmethod
    def shoot(self):
        pass

class GameWorld(GameObject):

    def __init__(self, id):
        super().__init__(id)
        self.create(0, 0)

    def getId(self):
        return self._id

    def create(self, x, y):
        pass

    def draw(self, x, y):
        pass

    def delete(self):
        pass

class Bullet(GameObject, Entity):

    def __init__(self, id, x, y):
        super().__init__(id)
        self.create(x, y)

    def getId(self):
        return self._id

    def create(self, x, y):
        self._X = x
        self._Y = y
        self.direction = gm.getPlayer().direction
        if self.direction == 'NONE':
            self.direction = 'RIGHT'
        self.draw(x, y)

    def draw(self, x, y):
        self._bullet_obj = gm.gw.canvas.create_oval(x - BULLET_SIZE/2, y - BULLET_SIZE/2,
                                                    x + BULLET_SIZE/2, y + BULLET_SIZE/2,
                                                    fill = 'blue')

    def delete(self):
        gm.deleteBullet(self.getId())

    def move(self, direction, step):
        if  direction == 'RIGHT':
            gm.gw.canvas.move(self._bullet_obj, step, 0)
            self._X = self._X + step
        if  direction == 'LEFT':
            gm.gw.canvas.move(self._bullet_obj, -step, 0)
            self._X = self._X - step
        if  direction == 'UP':
            gm.gw.canvas.move(self._bullet_obj, 0, -step)
            self._Y = self._Y - step
        if  direction == 'DOWN':
            gm.gw.canvas.move(self._bullet_obj, 0, step)
            self._Y = self._Y + step

    @property
    def getX(self):
        return self._X

    @property
    def getY(self):
        return self._Y

    def shoot(self):
        pass

class Player(GameObject, Entity):

    def __init__(self, id, x, y):
        super().__init__(id)
        self.create(x, y)

    def getId(self):
        return self._id

    def create(self, x, y):
        self._X = x
        self._Y = y
        self.direction = 'NONE'

    def draw(self, x, y):
        self._player_obj = gm.gw.canvas.create_oval(x - PLAYER_SIZE/2, y - PLAYER_SIZE/2,
                                                   x + PLAYER_SIZE/2, y + PLAYER_SIZE/2,
                                                   fill = 'green')

    def delete(self):
        pass

    def move(self, direction, step):
        if (direction == 'RIGHT' and
            self._X + step + PLAYER_SIZE / 2 < GAME_WIDTH):
            gm.gw.canvas.move(self._player_obj, step, 0)
            self._X = self._X + step
        if (direction == 'LEFT' and
            self._X - step - PLAYER_SIZE / 2 > 0):
            gm.gw.canvas.move(self._player_obj, -step, 0)
            self._X = self._X - step
        if (direction == 'UP' and
            self._Y - step - PLAYER_SIZE / 2 > 0):
            gm.gw.canvas.move(self._player_obj, 0, -step)
            self._Y = self._Y - step
        if (direction == 'DOWN' and
            self._Y + step + PLAYER_SIZE / 2 < GAME_HEIGHT):
            gm.gw.canvas.move(self._player_obj, 0, step)
            self._Y = self._Y + step

    def shoot(self):
        pass

    @property
    def getX(self):
        return self._X

    @property
    def getY(self):
        return self._Y

class Enemy(GameObject, Entity):

    def __init__(self, id, x, y):
        super().__init__(id)
        self.create(x, y)

    def getId(self):
        return self._id

    def create(self, x, y):
        self._X = x
        self._Y = y
        self.direction = 'NONE'

    def draw(self, x, y):
        self._enemy_obj = gm.gw.canvas.create_oval(x - ENEMY_SIZE/2, y - ENEMY_SIZE/2,
                                 x + ENEMY_SIZE/2, y + ENEMY_SIZE/2,
                                 fill = 'red')

    def delete(self):
        pass

    def move(self, direction, step):
        if (direction == 'RIGHT' and
            self._X + step + PLAYER_SIZE / 2 < GAME_WIDTH):
            gm.gw.canvas.move(self._enemy_obj, step, 0)
            self._X = self._X + step
        if (direction == 'LEFT' and
            self._X - step - PLAYER_SIZE / 2 > 0):
            gm.gw.canvas.move(self._enemy_obj, -step, 0)
            self._X = self._X - step
        if (direction == 'UP' and
            self._Y - step - PLAYER_SIZE / 2 > 0):
            gm.gw.canvas.move(self._enemy_obj, 0, -step)
            self._Y = self._Y - step
        if (direction == 'DOWN' and
            self._Y + step + PLAYER_SIZE / 2 < GAME_HEIGHT):
            gm.gw.canvas.move(self._enemy_obj, 0, step)
            self._Y = self._Y + step

    def shoot(self):
        pass

    @property
    def getX(self):
        return self._X

    @property
    def getY(self):
        return self._Y



class ScoreBoard(GameObject):

    def __init__(self, id, x, y):
        super().__init__(id)
        self.create(x, y)

    def getId(self):
        return self._id

    def create(self, x, y):
        self._X = x
        self._Y = y

    def draw(self, x, y):
        self._score_obj = gm.gw.canvas.create_text(x, y, text = "Score")

    def delete(self):
        pass

class Timer:
    new_time = 0

    @staticmethod
    def getTime():
        return time.time()

    @staticmethod
    def setTime(t):
        Timer.new_time = t

class KeyboardManager:

    def rigthKeyPressed(self, keyCode):
        gm.getPlayer().direction = 'RIGHT'

    def leftKeyPressed(self, keyCode):
        gm.getPlayer().direction = 'LEFT'

    def downKeyPressed(self, keyCode):
        gm.getPlayer().direction = 'DOWN'

    def upKeyPressed(self, keyCode):
        gm.getPlayer().direction = 'UP'

    def spaceKeyPressed(self, keyCode):
        if len(gm.bullets):
            if Timer.getTime() - Timer.new_time > BULLET_INTERVAL:
                gm.createBullet(gm.getPlayer().getX, gm.getPlayer().getY)
        else:
            gm.createBullet(gm.getPlayer().getX, gm.getPlayer().getY)
            Timer.setTime(Timer.getTime())

class GameWindow(GameObject):

    def __init__(self, id):
        super().__init__(id)
        self.isPlaying = True

    def getId(self):
        return self._id

    def create(self, x, y):
        self.tk = Tk()
        self.tk.title('Game')

        # restrict window resize
        self.tk.resizable(0, 0)

        # overlapping game field
        self.tk.wm_attributes('-topmost', 1)

        # close window protocol
        self.tk.protocol("WM_DELETE_WINDOW", self.close_window)

        # key pressing bindings
        self.keyboard = KeyboardManager()

        self.tk.bind('<Right>', self.keyboard.rigthKeyPressed)
        self.tk.bind('<Left>', self.keyboard.leftKeyPressed)
        self.tk.bind('<Down>', self.keyboard.downKeyPressed)
        self.tk.bind('<Up>', self.keyboard.upKeyPressed)
        self.tk.bind('<space>', self.keyboard.spaceKeyPressed)

    def close_window(self):
        self.delete()

    def draw(self, x, y):
        # create new canvas for game
        self.canvas = Canvas(self.tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

        # each visible element will has it's own coords
        self.canvas.pack()

        # update canvas
        self.tk.update()

    def delete(self):
        self.tk.destroy()
        self.isPlaying = False



# windows, worlds, scoreBoards, players, enemies
gm = GameManager(1, 0, 1, 1, 1)
gm.draw()

directions = ['RIGHT', 'LEFT', 'DOWN', 'UP', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE',
              'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE']


# main loop
while gm.gw.isPlaying:


    for bul in gm.bullets:

        if (bul.getX > CANVAS_WIDTH + BULLET_SIZE or
            bul.getX < - BULLET_SIZE  or
            bul.getY > CANVAS_HEIGHT + BULLET_SIZE or
            bul.getY < - BULLET_SIZE):
            bul.delete()

        bul.move(bul.direction, BULLET_STEP)

    gm.getPlayer().move(gm.getPlayer().direction, PLAYER_STEP)

    gm.getEnemy().move(random.choice(directions), ENEMY_STEP)



    # update all idle_tasks
    gm.gw.tk.update_idletasks()

    # update all up to date
    gm.gw.tk.update()


    # sleep for a while
    time.sleep(0.01)
