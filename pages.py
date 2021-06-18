from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduccion(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        players_per_group = self.session.config['players_per_group']
        stages=self.session.config['stages']
        # Variables de tratamiento:
        # Tratamiento base: (baja competencia y baja información)
        treatment = 0
        # 1 Tratamiento con alta competencia y baja información
        if players_per_group==4 and stages==1:
            treatment = 1
        # 2 Tratamiento con baja competencia y alta información
        elif players_per_group==2 and stages==2:
            treatment = 2
        # 3 Tratamiento con alta competencia y alta información
        elif players_per_group==4 and stages==2:
            treatment = 3

        return dict(participant_id=self.participant.label, stages=stages, players_per_group=players_per_group,
                     treatment=treatment)

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

class Decision(Page):
    form_model = 'player'
    form_fields = ['inversion','units']

    def vars_for_template(self):
        players_per_group = self.session.config['players_per_group']
        stages=self.session.config['stages']

        # Variables de tratamiento:
        # Tratamiento base: (baja competencia y baja información)
        treatment = 0
        # 1 Tratamiento con alta competencia y baja información:
        if players_per_group==4 and stages==1:
            treatment = 1
        # 2 Tratamiento con baja competencia y alta información:
        elif players_per_group==2 and stages==2:
            treatment = 2
        # 3 Tratamiento con alta competencia y alta información
        elif players_per_group==4 and stages==2:
            treatment = 3
        return dict(participant_id=self.participant.label, stages=stages, players_per_group=players_per_group,
                     treatment=treatment)
    
    def before_next_page(self):
        player=self.player
        player.stage=player.stage+1

class ResultsWaitPage(WaitPage):
    body_text = "Espere que el otro participante responda, por favor."

    after_all_players_arrive ='set_payoffs'
    
class Resultados(Page):
    def vars_for_template(self):
        stages=self.session.config['stages']
        investment_cost=self.player.inversion*Constants.k
        return dict(stages=stages,other_player_units=self.player.other_player().units,investment_cost=investment_cost,other_player_inversion=self.player.other_player().inversion)

    def app_after_this_page(self,upcoming_apps):
        stages=self.session.config['stages']
        if self.round_number<Constants.num_rounds:
            if self.stages==1:
                return upcoming_apps[0]
        elif self.round_number==Constants.num_rounds:
            if self.stages==1:
                return upcoming_apps[-1]


class Resultados_finales(Page):
    def is_displayed(self):
        return self.round_number==Constants.num_rounds

    
page_sequence = [Introduccion, 
                Control_lectura,
                Decision, 
                ResultsWaitPage, 
                Resultados, 
                Decision, 
                ResultsWaitPage, 
                Resultados, 
                Resultados_finales]
