from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Move

class MoveForm(ModelForm):
    class Meta:
        model = Move
        exclude = []

    # def clean(self):
    #     x = self.cleared_data.get("x")
    #     y = self.cleared_data.get("y")
    #     game = self.instance.game
    #     try:
    #         if game.board()[x][y] is not None:
    #             raise ValidationError("square is not empty")
    #     except IndexError:
    #         raise ValidationError("Invalid Coordinates")
    #
    #     return self.cleared_data