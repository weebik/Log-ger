from third_party.sim_info import SimInfo

class SimReader:
    def __init__(self):
        self.sim = SimInfo()

    # gather data from sim
    def get_lap_data(self):
        lap_number = self.sim.graphics.completedLaps
        lap_time = self.sim.graphics.lastTime
        best_time = self.sim.graphics.bestTime
        fuel = self.sim.physics.fuel
        track_km = self.sim.graphics.distanceTraveled / 1000.0
        return lap_number, lap_time, best_time, fuel, track_km

    def get_track_name(self):
        return self.sim.static.track

    def get_car_model(self):
        return self.sim.static.carModel
    
    def close(self):
        self.sim.close()
