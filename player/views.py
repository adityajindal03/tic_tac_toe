# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from gameplay.models import Game
from .models import Invitation
from .forms import InvitationForm
@login_required
def home(request):
    all_my_games = Game.objects.game_for_user(request.user)
    active_games = all_my_games.active()
    invitations = request.user.invitation_recieved.all()
    return render(request , 'player/home.html',{'games':active_games,"invitations":invitations})

@login_required
def new_invitation(request):

    if request.method == "POST":
        invitation = Invitation(from_user = request.user)
        form = InvitationForm(instance = invitation,data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request,'player/new_invitation_form.html',{'form':form})
# Create your views here.

@login_required
def accept_invitations(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == "POST":
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player = invitation.to_user,
                second_player = invitation.from_user

            )
        invitation.delete()
        return redirect('player_home')
    else:
        print "inside else condition"
        print invitation
        return render(request,"player/accept_invitation_form.html",
                      {'invitation':invitation}
                      )

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')