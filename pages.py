from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduccion(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        players_per_group = self.session.config['players_p_group']
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
        players_per_group = self.session.config['players_p_group']
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
        


class ResultsWaitPage_inversion(WaitPage):
    
    body_text = "Espere que el otro participante responda, por favor."


    after_all_players_arrive= 'set_payoffs'

class Resultados_inversion(Page):

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

    

class Decision_cantidad(Page):
    def is_diplayed(self):
        stages=self.session.config['stages']
        return stages==2

    form_model = 'player'
    form_fields = ['units']

    def vars_for_template(self):
        players_per_group = self.session.config['players_p_group']
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

class ResultsWaitPage_cantidad(WaitPage):
    def is_diplayed(self):
        stages=self.session.config['stages']
        return stages==2
        
    body_text = "Espere que el otro participante responda, por favor."


    after_all_players_arrive= 'set_payoffs'

    
class Resultados_cantidad(Page):
    def is_diplayed(self):
        stages=self.session.config['stages']
        return stages==2

    def vars_for_template(self):
        stages=self.session.config['stages']
        inversion=self.player.inversion
        investment_cost=inversion*inversion*Constants.k
        player=self.player
        stage=player.stage

        players_per_group = self.session.config['players_p_group']
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




class Resultados_finales(Page):
    def is_displayed(self):
        return self.round_number==Constants.num_rounds
    
    def vars_for_template(self):
        players_per_group = self.session.config['players_p_group']
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
                ResultsWaitPage_inversion, 
                Resultados_inversion, 
                Decision_cantidad, 
                ResultsWaitPage_cantidad, 
                Resultados_cantidad, 
                Resultados_finales]
