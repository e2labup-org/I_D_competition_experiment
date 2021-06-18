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
    #players_per_group = None
    #stages=2
    num_rounds = 2
    max_units_per_player=10
    instructions_template = 'innovation_game/instrucciones.html'
    alpha=30
    players_per_group=4
    total_capacity = 70 #precio máximo del producto
    #max_units_per_player = int(total_capacity / players_per_group)
    max_investment=8
    max_units_cost=20
    k=1.5 #un parámetro para la inversión


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    total_units = models.IntegerField(doc="""Total de unidades producidas por todos los jugadores""")

    unit_price=models.CurrencyField()

    total_inversion = models.IntegerField(doc="""Total de inversión por todos los jugadores""")



    def set_payoffs(self):
        """
        Función para obtener las ganancias en cada ronda y asignarle a cada jugador su beneficio propio de la ronda.
        Se hallan las unidades totales entre players de la ronda, para así hallar un precio por el producto.
        """
        stages=self.session.config['stages']
        total_players=Constants.players_per_group
        players=self.get_players()
        

        if stages==2:

                self.total_units = sum([p.units for p in players])
                self.unit_price = Constants.total_capacity - self.total_units
                for p in players:
                    p.payoff = (self.unit_price-Constants.max_units_cost+p.inversion) * p.units - p.inversion*p.inversion*Constants.k
           
        elif stages==1:
                
                self.total_inversion=sum([p.inversion for p in players])
                for p in players:
                    if total_players==2:
                        p.payoff=25*(Constants.alpha+total_players*p.inversion+p.inversion-self.total_inversion)*(Constants.alpha+total_players*p.inversion+p.inversion-self.total_inversion)-225*Constants.k*p.inversion*p.inversion
                    if total_players==4:
                        p.payoff=9*(Constants.alpha+total_players*p.inversion+p.inversion-self.total_inversion)*(Constants.alpha+total_players*p.inversion+p.inversion-self.total_inversion)-225*Constants.k*p.inversion*p.inversion

            

class Player(BasePlayer):
    total_units = models.IntegerField(doc="""Total de unidades producidas por todos los jugadores""")
    total_inversion = models.IntegerField(doc="""Total de unidades invertidas por todos los jugadores""")
    unit_price=models.CurrencyField()

    inversion = models.IntegerField(
        initial=0,
        min=0,
        max=Constants.max_investment,
        label="¿Cuánto deseas invertir?",
        doc="""Cantidad de unidades para invertir"""
    )

    units = models.IntegerField(
        initial=0,
        min=0,
        max=Constants.max_units_per_player,
        doc="""Cantidad de unidades para producir""",
        label="¿Cuánto deseas producir?"
    )

    def other_player(self):
        return self.get_others_in_group()[0]
    
    stage = models.IntegerField(
        initial=0,
        min=0
    )

    def other_player_sum_inversion(self):
        others=self.get_others_in_group()
        sum_others_inversion=[]
        for p in others:
            inversion=p.inversion
            sum_others_inversion.append(inversion)
        
        sum_other_inversion=round(sum(sum_others_inversion))
        return sum_other_inversion
    
    def other_player_sum_units(self):
        others=self.get_others_in_group()
        sum_others_units=[]
        for p in others:
            inversion=p.inversion
            sum_others_units.append(inversion)
        
        sum_other_units=round(sum(sum_others_units))
        return sum_other_units
    
    def set_payoffs_for_4_players(self):
        stages=self.session.config['stages']
        sum_inversion=self.other_player_sum_inversion()
        players=Constants.players_per_group
        self.total_inversion=players*sum_inversion+self.inversion
        sum_units=self.other_player_sum_units()
        self.total_units=players*sum_units+self.units
        if stages==2:
            self.unit_price = Constants.total_capacity - self.total_units
            self.payoff = (self.unit_price-Constants.max_units_cost+self.inversion) * self.units - self.inversion*self.inversion*Constants.k
           
        elif stages==1:
            self.payoff=9*(Constants.alpha+players*self.inversion+self.inversion-self.total_inversion)*(Constants.alpha+players*self.inversion+self.inversion-self.total_inversion)-225*Constants.k*self.inversion*self.inversion


    """
    Variables para el survey:
    """
    pregunta1=models.IntegerField(label="""
    En la primera etapa inviertes 4 unidades,
    ¿Cuánto es tu costo unitario después de la primera etapa?""",
    )

    pregunta2=models.IntegerField(label="""
    En la segunda etapa eliges una cantidad de 10, mientras que el otro jugador elige 4.
    ¿Cuánto es tu precio?
    """)

    pregunta3=models.IntegerField(label="""
    En la segunda etapa eliges una
    cantidad de 3, mientras que el otro jugador elige 4.
    ¿Cuánto es tu precio?
    """)

    pregunta4=models.IntegerField(label="""
    En la primera etapa inviertes 8, en la segunda etapa eliges una
    cantidad de 7, mientras que el otro jugador elige 9.
    ¿Cuánto es tu ganancia?    
    """)

    pregunta5=models.BooleanField(label="""
    En cualquiera de los periodos, dada una cantidad del otro jugador,
    si eliges mayor cantidad para producir, tu precio es menor
    """)
