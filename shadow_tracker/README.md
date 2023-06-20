Development of an API to track shadow casts caused by certain objects over the months.

In this first version, the coordinates and interval parameters must be edited directly in the code in the shadow_plot.py module

    ...
    # set parameters 
    hours = range(6, 19)
    days = range(1, 2)
    months = range(1, 13)
    year = 2023
    time_zone = -3
    location = (-22.814519, -42.940407)
    ...


ext/sunpos.py - module containing the basis of the algorithm for astronomical calculations.

    python ext/sunpos.py

shadow_plot.py - module developed to be an API and provide structured data for plotting graphs.

    python shadow_plot.py

draw_animate.py - module used to test the shadow_plot API, through an animated simulation.

    python draw_animete.py

plot.py - It plots the graphical representation of all points of the simulation defining the maximum and minimum points of the projection.

    python plot.py