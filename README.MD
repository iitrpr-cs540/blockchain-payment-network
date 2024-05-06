## Steps to set up

```
    git clone https://github.com/aggarwal-aditya/blockchain_project.git
```

1. Create virtual environment and install the requirements 

```
    python -m venv env
    source -m env/bin/activate    
    pip install -r requirements.txt
```

2. Create graphs

```
    python generate_graph.py (for generating a single graph)
    python automate_graph_gen.py (for generating multiple graphs)
```

Run simulation.py to run the simulation on the network

There are two toggle switches present in the code 
1. (give_second_chance = True)in simulation.py, which allows us to use our proposed second chance algorithm. (Turn to False to use the algorithm implemented in the paper)
2. (additive_incerment = True) in network.py, which allows one to change probability updation mechanisms (More details in report)
