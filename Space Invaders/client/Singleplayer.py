import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import Qt, QTimer, QRect

from Entities.Alien import Alien
from Entities.Bullet import Bullet
from Entities.Player import Player
from Database import Storage
from Entities.Shield import Shield

from time import  sleep

import random


class StartGameSingleplayer(QMainWindow):
    counter = 0


    def __init__(self):
        super().__init__()
        self.total_point = 0
        self.bullets = []
        self.bullets_enemy = []
        self.aliens = []
        self.shields = []
        self.init_ui()


    def init_ui(self):
        self.init_window()
        self.labels()
        self.init_aliens()

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.init_alien_attack)
        self.timer2.start(1200)

        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.alien_attack)
        self.timer3.start(60)

        self.init_shield()
        self.player = Player(self, 'images/spacecraft.png', 15, 655, 131, 91)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.attack)
        self.timer1.timeout.connect(self.destroy_enemy)




    def init_window(self):
        self.setFixedSize(950, 778)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Space Invaders [singleplayer mode]')

        self.bgLabel = QLabel(self)
        self.background = QPixmap('images/bg-resized2.jpg')
        self.bgLabel.setPixmap(self.background)
        self.bgLabel.setGeometry(0, 0, 950, 778)

    def init_aliens(self):
        for i in range(11):
            self.aliens.append(Alien(self, 'images/alienn-resized.png', 50 + 70 * i, 86, 67, 49))
            self.aliens.append(Alien(self, 'images/alien2-resized.png', 50 + 70 * i, 155, 50, 45))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 205, 50, 45))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 255, 50, 45))
            self.aliens.append(Alien(self, 'images/alien3-resized.png', 50 + 70 * i, 305, 50, 45))

        self.set_timer = 500
        timer = QTimer(self)
        timer.timeout.connect(self.on_timeout)
        timer.start(self.set_timer)

    def init_shield(self):
        for i in range (4):
            self.shields.append(Shield(self, 'images/shield.png', 50 + 260 * i, 546, 85, 105))
        """""
        self.set_timer = 500
        timer = QTimer(self)
        timer.timeout.connect(self.on_timeout)
        timer.start(self.set_timer)
        """""
    def on_timeout(self):
        if self.counter == 3:
            for alien in self.aliens:
                alien.move_down()
            self.set_timer -= 200
            self.counter = 0

        if self.aliens[0].direction_left:
            for alien in self.aliens:
                alien.move_left()
            if self.aliens[0].x - 20 < 10:
                self.counter += 1
                Alien.direction_left = False
        else:
            for alien in self.aliens:
                alien.move_right()
            if self.aliens[len(self.aliens) - 1].x + 20 > 900:
                Alien.direction_left = True

    def labels(self):
        self.pause_label = QLabel(self)
        self.pause_label.setText("pause [p]")
        self.pause_label.setGeometry(QRect(850, 750, 101, 31))
        self.pause_label.show()

        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)

        self.pause_label.setFont(font)
        self.pause_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pause_label.setAlignment(Qt.AlignCenter)

        self.lives1_label = QLabel(self)
        self.lives1 = QPixmap('images/lives.png')
        self.lives1_label.setPixmap(self.lives1)
        self.lives1_label.setGeometry(QRect(10, 10, 31, 31))

        self.lives2_label = QLabel(self)
        self.lives2 = QPixmap('images/lives.png')
        self.lives2_label.setPixmap(self.lives2)
        self.lives2_label.setGeometry(QRect(40, 10, 31, 31))

        self.lives3_label = QLabel(self)
        self.lives3 = QPixmap('images/lives.png')
        self.lives3_label.setPixmap(self.lives3)
        self.lives3_label.setGeometry(QRect(70, 10, 31, 31))

        self.score_label = QLabel(self)
        self.score_label.setText("score: ")
        self.score_label.setGeometry(QRect(840, 30, 61, 31))
        self.score_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font: 75 15pt \"Fixedsys\";")

        self.hiscore_label = QLabel(self)
        self.hiscore_label.setText("highscore: ")
        self.hiscore_label.setGeometry(QRect(800, 10, 111, 20))
        self.hiscore_label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")


        self.hi_score = QLabel(self)
        self.hi_score.setText('0')
        self.hi_score.setGeometry(QRect(910, 10, 111, 21))
        self.hi_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Fixedsys\";")

        self.score = QLabel(self)
        self.score.setText(str(self.total_point))
        self.score.setGeometry(QRect(910, 40, 111, 16))
        self.score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 75 15pt \"Fixedsys\";")

        self.current_level = QLabel(self)
        self.current_level.setText("Current level: ")
        self.current_level.setGeometry(QRect(420, 10, 111, 20))
        self.current_level.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")

        self.current_score = QLabel(self)
        self.current_score.setText("0")
        self.current_score.setGeometry(QRect(540, 10, 111, 20))
        self.current_score.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "font: 75 15pt \"Fixedsys\";")
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.player.move_left()
        elif event.key() == Qt.Key_D:
            self.player.move_right()
        elif event.key() == Qt.Key_Space:
            self.bullets.append(Bullet(self, 'images/bullett.png', self.player.x + 8, self.player.y - 23, 45, 45))
            self.timer1.start(10)
    """""
    def init_alien_attack(self):
        for i in range(11):
            napadac = random.randint(0, 55)
            self.bullets_enemy.append(Bullet(self, 'images/bullett.png', self.aliens[napadac].x - 8, self.aliens[napadac].y + 23, 45, 45))
            self.timer1.start(10)
    """

    def init_alien_attack(self):
        napadac = random.randint(0, 54)
        self.bullets_enemy.append(Bullet(self, 'images/bullett.png', self.aliens[napadac].x - 8, self.aliens[napadac].y + 23, 45, 45))

    def alien_attack(self):

        for bullet in self.bullets_enemy:
            bullet.move_down()



    def destroy_enemy(self):
        for bullet in self.bullets:
            for alien in self.aliens:
                if bullet.x > alien.x and bullet.x < alien.x + 45:
                    if bullet.y > alien.y and bullet.y < alien.y + 45:
                            bullet.avatar.hide()
                            self.bullets.remove(bullet)
                            alien.avatar.hide()
                            self.aliens.remove(alien)


    def attack(self):
        count_shield0 = 0
        count_shield1 = 0
        count_shield2 = 0
        count_shield3 = 0
        for bullet in self.bullets:
            bullet.move_up()
            # ovo moram da doradim ne radi bas dobro, treba mi neki brojac ???
            for shield in self.shields:
                    if bullet.x > 50 and bullet.x < 135:
                        count_shield0  += 1

                        if count_shield0 == 1:
                            self.shields[0].avatar.hide()
                            self.shield0 = Shield(self, 'images/shield2.png', 50, 546, 85, 105)
                            bullet.avatar.hide()
                            #self.bullets.remove(bullet)
                            self.score.setText(str(self.total_point + 10))

                        if count_shield0 == 2:
                            self.shield0.avatar.hide()
                            self.shield4 = Shield(self, 'images/lives.png', 50, 546, 85, 105)
                            bullet.avatar.hide()
                            #self.bullets.remove(bullet)
                            self.score.setText(str(self.total_point + 10))

                        if count_shield0 == 3:
                            self.shield4.avatar.hide()
                            self.shield8 = Shield(self, 'images/icon.png', 50, 546, 85, 105)
                            bullet.avatar.hide()
                            #self.bullets.remove(bullet)
                            self.score.setText(str(self.total_point + 10))

                        if count_shield0 == 4:
                            self.shield8.avatar.hide()
                            #self.shield8 = Shield(self, 'images/icon.png', 50, 546, 85, 105)
                            bullet.avatar.hide()
                            #self.bullets.remove(bullet)
                            #self.score.setText(str(self.total_point + 10))




                    if bullet.x > 310 and bullet.x < 395:
                        self.shields[1].avatar.hide()
                        self.shield1 = Shield(self, 'images/lives.png', 310, 546, 85, 105)
                        bullet.avatar.hide()
                        self.score.setText(str(self.total_point + 10))
                    if bullet.x > 570 and bullet.x < 655:
                        self.shields[2].avatar.hide()
                        self.shield2 = Shield(self, 'images/lives.png', 570, 546, 85, 105)
                        bullet.avatar.hide()
                        self.score.setText(str(self.total_point + 10))
                    if bullet.x > 830 and bullet.x < 915:
                        self.shields[3].avatar.hide()
                        self.shield3 = Shield(self, 'images/lives.png', 830, 546, 85, 105)
                        bullet.avatar.hide()
                        self.score.setText(str(self.total_point + 10))







if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = StartGameSingleplayer()
    sys.exit(app.exec_())
