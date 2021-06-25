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
    players_per_group=None
    total_capacity = 70 #precio máximo del producto
    #max_units_per_player = int(total_capacity / players_per_group)
    max_investment=8
    max_units_cost=20
    k=1.5 #un parámetro para la inversión


class Subsession(BaseSubsession):
    
    def creating_session(self):
        players_p_group=self.session.config['players_p_group']
        matriz=[]
        players=self.get_players() #lista jugadores
        numero_grupos=len(players)/players_p_group
        i=0
        for p in range(int(numero_grupos)):
            matriz.append([])
            for j in range(players_p_group):
                matriz[p].append(players[i])
                i=i+1

        
        self.set_group_matrix(matriz)
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
        players_p_group=self.session.config['players_p_group']
        players=self.get_players()
        

        
        for p in players:
 
            #Para este punto hay que hacer un "for" que agregue c/u de los otros jugadores en una lista y hacer el average.
            if stages==2:
                other_players_units=p.get_others_in_group()[0].units
                units_otros=round(other_players_units/(len(players)-1))
                self.total_units = units_otros+p.units
                self.unit_price = Constants.total_capacity - self.total_units
                p.payoff = (self.unit_price-Constants.max_units_cost+p.inversion) * p.units - p.inversion*p.inversion*Constants.k
           
            elif stages==1:
                other_players_inversion=p.get_others_in_group()[0].inversion #solo llama a 1 de los posibles 3
                inversion_otros=round(other_players_inversion/(len(players)-1))
                self.total_inversion=inversion_otros+p.inversion
                if players_p_group==2:
                    p.payoff=25*(Constants.alpha+players_p_group*p.inversion+p.inversion-self.total_inversion)*(Constants.alpha+players_p_group*p.inversion+p.inversion-self.total_inversion)-225*Constants.k*p.inversion*p.inversion
                if players_p_group==4:
                    p.payoff=9*(Constants.alpha+players_p_group*p.inversion+p.inversion-self.total_inversion)*(Constants.alpha+players_p_group*p.inversion+p.inversion-self.total_inversion)-225*Constants.k*p.inversion*p.inversion

            

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
