# Cellular-automata based water simulation

from Parameters import Parameters
from SimulationState import SimulationState
from Visualizer import Visualizer

import time


class WaterSimulationManager:
    def __init__(self, params:Parameters):
        self.params = params
        self.sim_vis = Visualizer(params)
        self.sim_state = SimulationState(params)
    
    def run_sim(self):
        
        continue_running = True
        while continue_running:
            
            continue_running = self.sim_vis.update_screen(self.sim_state)
            
            self.sim_state.update_state()
            time.sleep(0.02)
            
def main():
    params = Parameters()
    sim = WaterSimulationManager(params)
    
    sim.run_sim()
    
if __name__ == '__main__':
    main()