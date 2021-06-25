# Competencia e I+D

## Sección 1:

El experimento tiene como objetivo ver, en un entorno de competencia bajo Cournot y la posibilidad de invertir en I+D, cómo afecta a la inversión si:
1. La competencia del mercado aumenta.
2. Los jugadores saben cuál va a ser la inversión de los otros jugadores,en otras palabras, si hay mayor información en el mercado.

## Sección 2:

Instalar otree  y python3

```
pip3 install -U otree
```

## Sección 3:

1. Tratamiento base: baja competencia y baja información
```
SESSION_CONFIGS = [
     dict(
        name='innovation_game',
        display_name="Innovation Game",
        num_demo_participants=2,
        app_sequence=['innovation_game'],
        stages=1,
        players_p_group=2
     ),
]
```

2. Tratamiento 1: alta competencia y baja información
```
SESSION_CONFIGS = [
     dict(
        name='innovation_game',
        display_name="Innovation Game",
        num_demo_participants=2,
        app_sequence=['innovation_game', 'payment_info'],
        stages=1,
        players_p_group=4
     ),
]
```

3. Tratamiento 2: baja competencia y alta información
```
SESSION_CONFIGS = [
     dict(
        name='innovation_game',
        display_name="Innovation Game",
        num_demo_participants=2,
        app_sequence=['innovation_game', 'payment_info'],
        stages=2,
        players_p_group=2
     ),
]
```

4. Tratamiento 3: alta competencia y alta información
```
SESSION_CONFIGS = [
     dict(
        name='innovation_game',
        display_name="Innovation Game",
        num_demo_participants=2,
        app_sequence=['innovation_game', 'payment_info'],
        stages=2,
        players_p_group=4
     ),
]
```

## Autora

* **Grecia Barandiaran Villegas** - *Trabajo inicial* - [Sweetdreamstome](https://github.com/Sweetdreamstome)



