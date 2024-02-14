# CRUD (Create Read Update Delete) operations

# Database representation
team: dict = {
    1: {"name": "John", "age": 20},
    3: {"name": "Mark", "age": 33},
    12: {"name": "Cavin", "age": 31},
}


# Application source code
def repr_players(players: dict):
    for number, player in players.items():
        print(f"\t[Player {number}]: {player['name']}, {player['age']}")


def player_add(name: str, age: int, number: int) -> None:
    if number in team:
        print("Player with the same number already exists")
        return

    team[number] = {"name": name, "age": age}


def player_delete(number: int) -> None:
    if number in team:
        del team[number]


def player_update(number: int, new_name: str, new_age: int) -> None:
    if number in team:
        team[number]["name"] = new_name
        team[number]["age"] = new_age


def main():
    operations = ("add", "del", "repr", "exit", "update")

    while True:
        operation = input("Please enter the operation: ")
        if operation not in operations:
            print(f"Operation: '{operation}' is not available\n")
            continue

        if operation == "exit":
            print("Bye!")
            break
        elif operation == "repr":
            repr_players(team)
        elif operation == "add":
            name = input("Enter player's name: ")
            age = int(input("Enter player's age: "))
            number = int(input("Enter player's number: "))
            player_add(name=name, age=age, number=number)
        elif operation == "del":
            number = int(input("Enter player's number to delete: "))
            player_delete(number=number)
        elif operation == "update":
            number = int(input("Enter player's number to update: "))
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            player_update(number=number, new_name=new_name, new_age=new_age)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    main()
