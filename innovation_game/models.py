from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = 'innovation_game'
    players_per_group = 2
    num_rounds = 2
    max_units_per_player=10
    instructions_template = 'innovation_game/instrucciones.html'

    # Total production capacity of all players
    total_capacity = 70
    #max_units_per_player = int(total_capacity / players_per_group)
    max_investment=8
    max_units_cost=20
    k=2


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)


class Group(BaseGroup):

   
    #def set_investment(self):
    #    players=self.get_players()
    #    for p in players:
    #     Player.investment_cost=Constants.k*Player.inversion

    total_units = models.IntegerField(doc="""Total units produced by all players""")

    unit_price=models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        self.total_units = sum([p.units for p in players])
        self.unit_price = Constants.total_capacity - self.total_units
        for p in players:
            p.payoff = self.unit_price * p.units

    


class Player(BasePlayer):

    inversion = models.IntegerField(
        min=0,
        max=Constants.max_investment,
        label="¿Cuánto deseas invertir?",
        doc="""Cantidad de unidades para invertir"""
    )

    units = models.IntegerField(
        min=0,
        max=Constants.max_units_per_player,
        doc="""Cantidad de unidades para producir""",
        label="¿Cuánto deseas producir?"
    )

    

    #investment_cost=models.IntegerField()
    
    def other_player(self):
        return self.get_others_in_group()[0]
    
    

  