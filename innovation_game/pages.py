from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduccion(Page):
    pass


class Decision_primeraetapa(Page):
    form_model = 'player'
    form_fields = ['inversion']


class ResultsWaitPage1(WaitPage):
    body_text = "Waiting for the other participant to decide."
    
class Resultados_primeraetapa(Page):
    def vars_for_template(self):
    
        investment_cost=self.player.inversion*Constants.k-self.player.inversion
        return dict(investment_cost=investment_cost,other_player_inversion=self.player.other_player().inversion)



class ResultsWaitPage2(WaitPage):
    body_text = "Waiting for the other participant to decide."

    after_all_players_arrive ='set_payoffs'

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups=True
    def after_all_players_arrive(subsession):
        subsession.group_randomly(fixed_id_in_group=True) #manten el id aun después del shuffle



class Decision_segundaetapa(Page):
    form_model = 'player'
    form_fields = ['units']


class Resultados_segundaetapa(Page):
    def vars_for_template(self):
        return dict(other_player_units=self.player.other_player().units)


page_sequence = [Introduccion, Decision_primeraetapa, ResultsWaitPage1, Resultados_primeraetapa, Decision_segundaetapa, ResultsWaitPage2, Resultados_segundaetapa, ShuffleWaitPage]
