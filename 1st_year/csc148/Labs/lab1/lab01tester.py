from lab01 import Race

if __name__ == '__main__':
    system = Race()
    system.add_runner("Gerhard", 40)
    system.add_runner("Tom", 30)
    system.add_runner("Toni", 20)
    system.add_runner("Margot", 30)
    system.add_runner("Gerhard", 30)
    
    print(system.get_runners_by_speed(30))