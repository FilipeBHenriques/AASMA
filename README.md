
# AASMA Project Group 19
- Duarte Costa 105787
- Lucas Raimundo 93114
- Filipe Henriques 95573

We implemented 3 variants of agents that play pokemon showdown locally against each other.
- A **Random Agent**, that makes random moves/switches and it's our baseline to evaluate the performance of the remaining agents. 
- A **Reactive Agent**, that attempts to inflict the maximum dmg to the opponent, if he can't cause damage he switches to the pokemon that has the highest damage against the opponent. 
- A **Proactive Agent**, takes into account the opponents available actions and the game plan, and aims to position itself advantageously for future turns. 

## Requirements and How to install
- git clone https://github.com/FilipeBHenriques/AASMA.git
- Install NodeJS https://nodejs.org/en/download
- Install Python3 3.10.0+
- cd AASMA; pip install -e poke-env

## How to run the server and the agents
- Run the server 
    - cd AASMA\pokemon-showdown
    - node pokemon-showdown
    - If you want the visual website with the games, click on the link http://localhost:8000

- Run the agents (args[1] -> number of battles)
    - cd AASMA\poke-env\examples
    - To run the Reactive vs Random: python testing_agents_reactive.py 5
    - To run the Proactive vs Random: python testing_agents_proactive.py 5
    - To run the Proactive vs Reactive: python testing_agents_proactive_vs_reactive.py 5
    
