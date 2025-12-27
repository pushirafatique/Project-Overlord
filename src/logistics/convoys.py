"""
Atlantic Convoy Logistics Module

This module simulates the routing, scheduling, and protection of trans‑Atlantic convoys
during the Second World War. It incorporates historical constraints such as U‑boat
threats, weather patterns, port capacities, and escort availability.
"""

import random
from typing import List, Dict, Tuple


class Convoy:
    """Represents a single convoy of merchant ships."""
    
    def __init__(self, convoy_id: str, departure_port: str, destination_port: str,
                 ships: int, cargo_value: float, escort_strength: float):
        self.convoy_id = convoy_id
        self.departure_port = departure_port
        self.destination_port = destination_port
        self.ships = ships
        self.cargo_value = cargo_value
        self.escort_strength = escort_strength  # 0.0–1.0, representing escort coverage
        self.position: float = 0.0  # progress along route (0.0–1.0)
        self.sunk_ships = 0
    
    def advance(self, threat_level: float) -> int:
        """
        Move the convoy one step along its route.
        Returns the number of ships lost in this step.
        """
        # Base progress influenced by weather and threat
        progress = random.uniform(0.05, 0.15) * (1.0 - threat_level * 0.5)
        self.position = min(1.0, self.position + progress)
        
        # Risk of U‑boat attack
        if random.random() < threat_level * (1.0 - self.escort_strength):
            losses = random.randint(1, max(1, int(self.ships * 0.1)))
            self.sunk_ships += losses
            self.ships -= losses
            return losses
        return 0
    
    def has_arrived(self) -> bool:
        return self.position >= 1.0


class ConvoyManager:
    """Orchestrates multiple convoys and allocates escorts."""
    
    def __init__(self):
        self.convoys: List[Convoy] = []
        self.total_sunk = 0
        self.total_arrived = 0
    
    def add_convoy(self, convoy: Convoy):
        self.convoys.append(convoy)
    
    def run_day(self, threat_level: float):
        """Simulate one day of convoy operations."""
        for convoy in self.convoys:
            if not convoy.has_arrived():
                sunk = convoy.advance(threat_level)
                self.total_sunk += sunk
                if convoy.has_arrived():
                    self.total_arrived += 1
    
    def get_statistics(self) -> Dict[str, float]:
        """Return summary statistics."""
        total_ships = sum(c.ships + c.sunk_ships for c in self.convoys)
        if total_ships == 0:
            return {}
        survival_rate = (sum(c.ships for c in self.convoys) / total_ships) * 100
        return {
            "active_convoys": len([c for c in self.convoys if not c.has_arrived()]),
            "arrived_convoys": self.total_arrived,
            "ships_sunk": self.total_sunk,
            "survival_rate_percent": survival_rate
        }


def plan_convoy_route(origin: str, destination: str) -> List[Tuple[float, float]]:
    """
    Generate a series of waypoints (longitude, latitude) for a typical
    North‑Atlantic convoy route, avoiding known U‑boat patrol areas.
    """
    # Simplified great‑circle approximation
    waypoints = [
        (origin, (45.0, -60.0)),
        ("Mid‑Atlantic", (50.0, -30.0)),
        ("Western Approaches", (55.0, -10.0)),
        (destination, (51.5, -0.1)),
    ]
    return waypoints


if __name__ == "__main__":
    # Example usage
    manager = ConvoyManager()
    manager.add_convoy(Convoy("HX‑229", "Halifax", "Liverpool", 45, 12.5e6, 0.7))
    manager.add_convoy(Convoy("SC‑122", "Sydney", "Liverpool", 38, 9.8e6, 0.6))
    
    for day in range(30):
        manager.run_day(threat_level=0.2)
    
    stats = manager.get_statistics()
    print("Convoy Logistics Simulation Results:")
    for key, val in stats.items():
        print(f"  {key}: {val}")