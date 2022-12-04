# Design a parking lot

# characters ---enter----> Content ----exit----> result

# vehicle ---enter---> Parking Spot ---exit---> Ticket

# Class Diagram

# class Vehicle
# attributes
# type: str
# name: str

# methods
# None

#------------------------------------------

# class Parking Spot
# attributes
# vehicle: Vehicle
# spotNumber: int
# level: Level
# available: boolean

# methods
# canFit(vehicle) -> Boolean
# takeSpot(vehicle) -> None
# leaveSpot(vehicle) -> None
# set_availability -> None

#------------------------------------------

# class Level
# attributes
# spotList: List[ParkingSpot]
# available_count: int
# available: Boolean

# method
# updateAvailableCount() -> void

#------------------------------------------

# class ParkingLot
# attributes
# name: str
# levels: int

# method
# enter(Vehichle) -> void
# findLevelAvailable() -> Level
# canVehicleFit(Vehicle) -> Boolean
# exit(Vehichle) -> Ticket
# check_availableCount(): int
# check_available(): boolean

#------------------------------------------

# Ticket
# attributes
# id
# amount
# vehicle
# enterTime
# exitTime
# status
# paymentMethod

from abc import ABC, abstractmethod
from enum import Enum

class Singleton:
    def singleton(class_):
        instances = {}
        def get_instances(*args, **kwargs):
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]
        return get_instances


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Vehicle(ABC):
    def __init__(self, size):
        self.size = size
        super().__init__()
    
    @abstractmethod
    def park(self):
        pass

class Motocycle(Vehicle):
    
    def park(self):
        print(f"A {self.size.name} motocycle is parked")
        
class Van(Vehicle):
    def park(self):
        print(f"A {self.size.name} van is parked")

class Truck(Vehicle):
    def park(self):
        print(f"A {self.size.name} truck is parked")
        
class ParkingSpot:
    def __init__(self, spot_id, level, size):
        self._vehicle = None
        self.spot_id = spot_id
        self.level = level
        self._availability = True
        self.size = size
        
    @property
    def vehicle(self):
        return self._vehicle

    def can_vehicle_fit(self, vehicle):
        return True if vehicle.size.value <= self.size.value else False

    def take_spot(self, vehicle):
        self._vehicle  = vehicle
        self._availability = False
    # leaveSpot(vehicle) -> None

    def leave_spot(self):
        self._vehicle = None
        self._availability = True

    # set_availability -> None
    @property
    def availability(self):
        return self._availability
        
class Level:
    def __init__(self, level_id):
        # assumption: every level has the same amout of spots
        self.level_id = level_id
        self.parking_spots_list = self.set_parking_spots()
        self._current_spot = None
        
    def set_parking_spots(self):
        parking_spots_list = []
        for i in range(1, 10):
            if i < 4:
                parking_spots_list.append(ParkingSpot(i, self.level_id, Size.SMALL))
            elif i < 7:
                parking_spots_list.append(ParkingSpot(i, self.level_id, Size.MEDIUM))
            else:
                parking_spots_list.append(ParkingSpot(i, self.level_id, Size.LARGE))
        return parking_spots_list

    def park_vehicle(self, vehicle):
        if self.is_available(vehicle):
            self._current_spot.take_spot(vehicle)
            ticket = Ticket(self.level_id, self._current_spot)
            return ticket

    def exit_vehicle(self, ticket):
        self._current_spot = ticket.parking_spot
        self._current_spot.leave_spot()
  
    def is_available(self, vehicle):
        for spot in self.parking_spots_list:
            if spot.can_vehicle_fit(vehicle) and spot.availability == True:
                self._current_spot = spot
                return True
        return False
    
    def get_available_spots(self, size):
        spot_cnt = 0
        for spot in self.parking_spots_list:
            if spot.size == size and spot.available == True:
                spot_cnt += 1
        return spot_cnt

@Singleton.singleton     
class ParkingLot:
    def __init__(self, level_number):
        self.level_number = level_number
        self.parking_levels = self._set_parking_levels()
    
    def _set_parking_levels(self):
        level_list = []
        for i in range(1, self.level_number):
            level_list.append(Level(i))
        return level_list

    def check_available(self, vehicle):
        for level in self.parking_levels:
            if level.is_available(vehicle):
                return True
        return False

    def park_vehicle(self, vehicle):
        for level in self.parking_levels:
            if level.is_available(vehicle):
                ticket = level.park_vehicle(vehicle)
                return ticket
        return None

    def exit_vehicle(self, ticket):
        parking_level = self.parking_levels[ticket.level]
        parking_level.exit_vehicle(ticket)

class Ticket:
    def __init__(self, level, parking_spot):
        self.level = level
        self.parking_spot = parking_spot
    



if __name__ == "__main__":
    parking_lot = ParkingLot(4)
    parking_lot1 = ParkingLot(10)
    print(parking_lot == parking_lot1)
    print(parking_lot.__dict__, parking_lot1.__dict__)
    small_motocycle = Motocycle(Size.SMALL)
    medium_van = Van(Size.MEDIUM)
    large_truck = Truck(Size.LARGE)
    ticket1 = parking_lot.park_vehicle(small_motocycle)
    ticket2 = parking_lot.park_vehicle(medium_van)
    ticket3 = parking_lot.park_vehicle(large_truck)
    print(ticket1.__dict__)
    print(ticket1.parking_spot.__dict__)
    parking_lot.exit_vehicle(ticket1)
    print(ticket1.parking_spot.__dict__)
    

    

