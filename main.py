import pymongo
from bson import ObjectId

class MongoDBManager:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['sports_management']
        self.sports_collection = self.db['sports']
        self.players_collection = self.db['players']

    def add_sport(self, sport_name, number_of_players, location, teams):
        sport_data = {
            "sport_name": sport_name,
            "number_of_players": number_of_players,
            "location": location,
            "teams": teams
        }
        result = self.sports_collection.insert_one(sport_data)
        print(f"Added sport with ID: {result.inserted_id}")

    def display_sports(self):
        sports = self.sports_collection.find()
        for sport in sports:
            print("\nName of Sport:", sport["sport_name"])
            print("Number of Players:", sport["number_of_players"])
            print("Match Location:", sport["location"])
            if sport["teams"]:
                print("Teams:")
                for team in sport["teams"]:
                    print(team)
            else:
                print("No teams added yet.")

    def delete_sport(self, sport_name):
        result = self.sports_collection.delete_one({"sport_name": sport_name})
        if result.deleted_count > 0:
            print(f"{sport_name} has been removed.")
        else:
            print("Sport not found.")

    def update_sport(self, sport_name, number_of_players=None, location=None, teams=None):
        update_data = {}
        if number_of_players:
            update_data["number_of_players"] = number_of_players
        if location:
            update_data["location"] = location
        if teams is not None:
            update_data["teams"] = teams

        result = self.sports_collection.update_one({"sport_name": sport_name}, {"$set": update_data})
        print(f"{sport_name}'s details have been updated.")
        
    def player_stats(self):
        pipeline = [
            {"$group": {
                "_id": None,
                "average_players": {"$avg": "$number_of_players"},
                "min_players": {"$min": "$number_of_players"},
                "max_players": {"$max": "$number_of_players"}
            }}
        ]
        result = list(self.sports_collection.aggregate(pipeline))
        if result:
            stats = result[0]
            print("\nPlayer Statistics Across All Sports:")
            print(f"Average number of players: {stats['average_players']:.2f}")
            print(f"Minimum number of players: {stats['min_players']}")
            print(f"Maximum number of players: {stats['max_players']}")
        else:
            print("No data available.")

    def add_player(self, name, team, sport, performances):
        player_data = {
            "name": name,
            "team": team,
            "sport": sport,
            "performances": performances
        }
        result = self.players_collection.insert_one(player_data)
        print(f"Added player with ID: {result.inserted_id}")

    def update_player_performance(self, player_id, new_performance):
        result = self.players_collection.update_one(
            {"_id": ObjectId(player_id)},
            {"$push": {"performances": new_performance}}
        )
        if result.modified_count > 0:
            print(f"Updated performance for player ID: {player_id}")
        else:
            print(" No changes made.")

    def display_player_performance(self, player_name):
        player = self.players_collection.find_one({"name": player_name})
        if player:
            print("\nPlayer Performance:")
            print("Name:", player["name"])
            print("Team:", player["team"])
            print("Sport:", player["sport"])
            print("Performances:")
            for performance in player["performances"]:
                print(performance)
        else:
            print("Player not found.")
def main():
    print("Sports Management System \n")
    manager = MongoDBManager()

    while True:
        print("\nMenu:")
        print("1. Add a new sport")
        print("2. Display all sports")
        print("3. Delete a sport")
        print("4. Update sport details")
        print("5. Player stats across all sports")
        print("6. Add a new player")
        print("7. Update player performance")
        print("8. Display player performance")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sport_name = input("Enter the name of sport: ")
            number_of_players = int(input("Enter the number of players: "))
            location = input("Enter the location: ")

            teams = []
            team_input = input("Enter team names separated by commas (or press enter to skip): ")
            if team_input:
                teams = [team.strip() for team in team_input.split(",")]

            manager.add_sport(sport_name, number_of_players, location, teams)

        elif choice == "2":
            manager.display_sports()

        elif choice == "3":
            sport_name = input("Enter the name of the sport to remove: ")
            manager.delete_sport(sport_name)

        elif choice == "4":
            sport_name = input("Enter the name of the sport to update: ")
            number_of_players = input("Enter the new number of players (or press enter to skip): ")
            number_of_players = int(number_of_players) if number_of_players.isdigit() else None
            
            location = input("Enter the new location (or press enter to skip): ")
            if location == "":
                location = None 

            team_input = input("Enter new team names separated by commas (or press enter to skip): ")
            teams = [team.strip() for team in team_input.split(",")] if team_input else None

            manager.update_sport(sport_name, number_of_players, location, teams)

        elif choice == "5":
            manager.player_stats()

        elif choice == "6":
            name = input("Enter player name: ")
            team = input("Enter player's team: ")
            sport = input("Enter the sport: ")
            performances = input("Enter performances separated by commas: ").split(",")
            performances = [performance.strip() for performance in performances]
            manager.add_player(name, team, sport, performances)

        elif choice == "7":
            player_id = input("Enter player ID to update performance: ")
            new_performance = input("Enter new performance: ")
            manager.update_player_performance(ObjectId(player_id), new_performance)

        elif choice == "8":
           player_name = input("Enter player name to display performance: ")
           manager.display_player_performance(player_name)
        elif choice == "9":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
