from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduccion(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        players_per_group = Constants.players_per_group
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

        return dict(stages=stages, 
                     players_per_group=players_per_group,
                     treatment=treatment)

class Control_lectura(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def error_message(self,values):
        print('values is',values)
        if values["pregunta1"] != 6:
            return 'La respuesta 1 está mal. Inténtelo de nuevo, por favor.'
        if values['pregunta2'] != 56:
            return 'La respuesta 2 está mal. Inténtelo de nuevo, por favor.'
        if values['pregunta3'] != 54:
            return 'La respuesta 3 está mal. Inténtelo de nuevo, por favor.'
        if values['pregunta4'] != 90:
            return 'La respuesta 4 está mal. Inténtelo de nuevo, por favor.'
        if values['pregunta5'] != True:
            return 'La respuesta 5 está mal. Inténtelo de nuevo, por favor.'

    form_model='player'
    form_fields=['pregunta1','pregunta2','pregunta3','pregunta4','pregunta5']

class Decision_inversion(Page):
    
    form_model = 'player'
    form_fields = ['inversion']

    def vars_for_template(self):
        players_per_group = Constants.players_per_group
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

        return dict(stages=stages, 
                     players_per_group=players_per_group,
                     treatment=treatment)
        
    def before_next_page(self):
        player=self.player
        stages=self.session.config['stages']
        if stages==2:
            player.stage=player.stage+1
        elif stages==1:
            player.stage=player.stage+10


class ResultsWaitPage(WaitPage):
    
    body_text = "Espere que el otro participante responda, por favor."
    
    """
    def before_next_page(self):
        players = Constants.players_per_group
        group=self.group
        player=self.player
        if players==2:
            return group.set_payoffs
        else:
            return player.set_payoffs_for_4_players
    """

    after_all_players_arrive= 'set_payoffs'

class Decision_cantidad(Page):
    def is_displayed(self):
        #solo saldrá cuando el tratamiento sea de 2 stages.
        player=self.player
        return player.stage<11


    form_model = 'player'
    form_fields = ['units']
    def vars_for_template(self):
        players_per_group = Constants.players_per_group
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

        return dict(stages=stages, 
                     players_per_group=players_per_group,
                     treatment=treatment)

    def before_next_page(self):
        #suma a la variable 'stage' para crear limitaciones a las páginas
        player=self.player
        player.stage=player.stage+1

    
class Resultados(Page):
    def is_displayed(self):
        player=self.player
        return player.stage<11

    def vars_for_template(self):
        stages=self.session.config['stages']
        inversion=self.player.inversion
        investment_cost=inversion*inversion*Constants.k
        player=self.player
        stage=player.stage

        players_per_group = Constants.players_per_group
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

        
        return dict(stages=stages,
                     stage=stage,
                     players_per_group=players_per_group,
                     treatment=treatment,
                     player=player,
                     other_player_units=self.player.other_player().units,
                     investment_cost=investment_cost,
                     other_player_inversion=self.player.other_player().inversion)

    def before_next_page(self):
        player=self.player
        stages=self.session.config['stages']
        if stages==1:
            player.stage=player.stage+1
        elif stages==2:
            player.stage=player.stage+10

"""
    def app_after_this_page(self,upcoming_apps):
        stages=self.session.config['stages']
        if self.round_number<Constants.num_rounds:
            if stages==1:
                return upcoming_apps[0]
        elif self.round_number==Constants.num_rounds:
            if stages==1:
                return upcoming_apps[-1]
"""

class Resultados_finales(Page):
    def is_displayed(self):
        return self.round_number==Constants.num_rounds
    
    def vars_for_template(self):
        players_per_group = Constants.players_per_group
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

        return dict(stages=stages, 
                     players_per_group=players_per_group,
                     treatment=treatment)

    
page_sequence = [Introduccion, 
                #Control_lectura,
                Decision_inversion, 
                ResultsWaitPage, 
                Resultados, 
                Decision_cantidad, 
                ResultsWaitPage, 
                Resultados, 
                Resultados_finales]
