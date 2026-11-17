import re

RATES = {"bike": 10, "car": 30, "truck": 60}

def minutes_parked(times):
    if not isinstance(times, str):
        return None
    match = re.fullmatch(r"([0-9]{1,2}):([0-9]{2})-([0-9]{1,2}):([0-9]{2})", times.strip())
    if not match:
        return None
    h1, m1, h2, m2 = map(int, match.groups())
    if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
        return None
    minutes = (h2 * 60 + m2) - (h1 * 60 + m1)
    if minutes < 0:
        return None
    return minutes

def hourly_rate(vehicle):
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())

def format_plate(plate):
    if not isinstance(plate, str):
        return None
    p = "".join(plate.split())
    if not re.fullmatch(r"[A-Za-z]{2}[0-9]{2}[A-Za-z]{2}[0-9]{4}", p):
        return None
    p = p.upper()
    return p[0] + p[1] + " " + p[2:4] + " " + p[4:6] + " " + p[6:10]

def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result)

if __name__ == "__main__":
    main()
