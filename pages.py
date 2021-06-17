from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduccion(Page):
    def is_displayed(self):
        return self.round_number == 1

class Control_lectura(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def error_message(self,values):
        print('values is',values)
        if values["pregunta1"] != 6:
            return 'Esa no es la respuesta. Inténtelo de nuevo, por favor.'
        if values['pregunta2'] != 56:
            return 'Esa no es la respuesta. Inténtelo de nuevo, por favor.'
        if values['pregunta3'] != 54:
            return 'Esa no es la respuesta. Inténtelo de nuevo, por favor.'
        if values['pregunta4'] != 90:
            return 'Esa no es la respuesta. Inténtelo de nuevo, por favor.'
        if values['pregunta5'] != True:
            return 'Esa no es la respuesta. Inténtelo de nuevo, por favor.'
    
    

    form_model='player'
    form_fields=['pregunta1','pregunta2','pregunta3','pregunta4','pregunta5']

class Decision_primeraetapa(Page):
    form_model = 'player'
    form_fields = ['inversion']

class ResultsWaitPage1(WaitPage):
    body_text = "Espere que el otro participante responda, por favor."
    
class Resultados_primeraetapa(Page):
    def vars_for_template(self):
    
        investment_cost=self.player.inversion*Constants.k
        return dict(investment_cost=investment_cost,other_player_inversion=self.player.other_player().inversion)

class Decision_segundaetapa(Page):
    form_model = 'player'
    form_fields = ['units']

class ResultsWaitPage2(WaitPage):
    body_text = "Espere que el otro participante responda, por favor."

    after_all_players_arrive ='set_payoffs'

class Resultados_segundaetapa(Page):
    def vars_for_template(self):
        return dict(other_player_units=self.player.other_player().units)

class Resultados_finales(Page):
    def is_displayed(self):
        return self.round_number==Constants.num_rounds

    
page_sequence = [Introduccion, Control_lectura, Decision_primeraetapa, ResultsWaitPage1, Resultados_primeraetapa, Decision_segundaetapa, ResultsWaitPage2, Resultados_segundaetapa, Resultados_finales]
