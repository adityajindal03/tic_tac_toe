# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator , MinValueValidator
BOARD_SIZE = 3

# Create your models here.

GAME_STATUS_CHOICES = (
    ('F',"First Player To Move"),
    ('S',"Second PLayer To Move"),
    ('W',"First Player To Win"),
    ('L',"Second Player To Win"),
    ('D',"Draw"),
    ('FS',"Finished")


)



class GameQuerySet(models.QuerySet):
    def game_for_user(self, user):
        return self.filter(Q(first_player = user) | Q(second_player = user))

    def active(self):

        return self.filter(Q(status = "F") | Q(status = "S"))


@python_2_unicode_compatible
class Game(models.Model):
    first_player = models.ForeignKey(User,related_name = "game_first_player")
    second_player = models.ForeignKey(User,related_name = "game_second_player")
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,default = 'F',choices=GAME_STATUS_CHOICES)

    objects = GameQuerySet.as_manager()

    def __str__(self):

        return str(self.first_player)+" vs "  + str(self.second_player)

    def get_absolute_url(self):
        return reverse("gameplay_detail",args=[self.id])

    def board(self):


        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for a_move in self.move_set.all():
            board[a_move.x][a_move.y]  = a_move

        return board

    def is_users_move(self,user):
        return (user == self.first_player and self.status == "F") or (user == self.second_player and self.status == "S")



    def new_move(self):

        if self.status not in 'FS':
            raise ValueError("Cannot make move on finished game")

        return Move(game=self,by_first_player = self.status == 'F')


    def update_after_move(self, move):

        status = self._get_game_status_after_move(move)
        print status
        self.status = status
    def _get_game_status_after_move(self,move):
        x, y = move.x , move.y
        board = self.board()
        print board
        if board[y][0] and board[y][1] and board[y][2]:
            if board[y][0] == board[y][1] == board[y][2]:
                return "W" if move.by_first_player else "L"
        if board[0][x] and board[1][x] and board[2][x]:
            if board[0][x] == board[1][x] == board[2][x]:
                return "W" if move.by_first_player else "L"
        if board[0][0] and board[1][1] and board[2][2]:
            if board[0][0] == board[1][1] == board[2][2]:
                return "W" if move.by_first_player else "L"

        if board[0][2] and board[1][1] and board[2][0]:
            if board[0][2] == board[1][1] == board[2][0]:
                return "W" if move.by_first_player else "L"


        if len(self.move_set.all()) >= BOARD_SIZE**2:
            return 'D'
        return 'S' if self.status == 'F' else 'F'




class Move(models.Model):
    x = models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(BOARD_SIZE-1)])
    y = models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(BOARD_SIZE-1)])
    comment = models.CharField(max_length = 300,blank = True)
    by_first_player = models.BooleanField(editable=False)
    game = models.ForeignKey(Game,on_delete = models.CASCADE,editable=False)




    def save(self,*args,**kwargs):
        super(Move,self).save(*args,**kwargs)
        self.game.update_after_move(self)
        self.game.save()

    def __eq__(self,other):

        if other is None:
            print "inside other part"
            return False
        if self is None:
            print "inside self part"
            return False

        print "outside other part"
        print other
        return other.by_first_player == self.by_first_player



