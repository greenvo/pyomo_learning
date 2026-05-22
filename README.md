# pyomo_learning
A simple example of how opbject oriented programming works

We develop a minimalist example of the solver at hand. Aim here is to plan how the solver will be called and how it will be used in deployment.

Separation of Concerns.

1 . MMO modules

MMO using Pyomo provides a modular approach to building a solver. The solver within its complexity for staff without the concern of the optimisation can be viewed as a custom greenvoltis limited scope library

2. MMO infra

Infrastructure that runs the MMO and shares the results with other modules. This module is also responsible for assembling the correct modular blocks.
