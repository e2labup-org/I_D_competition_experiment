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

    
    total_capacity = 70 #precio máximo del producto
    #max_units_per_player = int(total_capacity / players_per_group)
    max_investment=8
    max_units_cost=20
    k=1.5 #un parámetro para la inversión


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


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

    def other_player(self):
        return self.get_others_in_group()[0]


    """
    Variables para el survey:
    """
    pregunta1=models.IntegerField(label="""
    En la primera etapa inviertes 4 unidades,
    ¿Cuánto es tu costo unitario después de la primera etapa?""",
    )

    pregunta2=models.IntegerField(label="""
    En la primera etapa inviertes 3 unidades, en la segunda etapa
    eliges una cantidad de 10, mientras que el otro jugador elige 4.
    ¿Cuánto es tu precio?
    """)

    pregunta3=models.IntegerField(label="""
    En la primera etapa inviertes 6, en la segunda etapa eliges una
    cantidad de 3, mientras que el otro jugador elige 4.
    ¿Cuánto es tu precio?
    """)

    pregunta4=models.IntegerField(label="""
    En la primera etapa inviertes 8, en la segunda etapa eliges una
    cantidad de 7, mientras que el otro jugador elige 9.
    ¿Cuánto es tu precio?    
    """)

    pregunta5=models.BooleanField(label="""
    En cualquiera de los periodos, dada una cantidad del otro jugador,
    si eliges mayor cantidad para producir, tu precio es menor
    """)
    
    

  