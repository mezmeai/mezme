from crypto_oracle_platform import CryptoOraclePlatform

class UserInterface:
    def __init__(self):
        self.platform = CryptoOraclePlatform()

    def run(self):
        while True:
            print("\n1. Deploy Agent\n2. Run Agent\n3. List Agents\n4. Delete Agent\n5. Exit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                name = input("Enter agent name: ")
                config = json.loads(input("Enter agent configuration (JSON format): "))
                self.platform.deploy_agent(name, config)
            elif choice == "2":
                name = input("Enter agent name to run: ")
                data = json.loads(input("Enter data to process (JSON format): "))
                result = self.platform.run_agent(name, data)
                print(f"Result: {result}")
            elif choice == "3":
                print(json.dumps(self.platform.list_agents(), indent=2))
            elif choice == "4":
                name = input("Enter agent name to delete: ")
                self.platform.delete_agent(name)
            elif choice == "5":
                print("Exiting the platform.")
                break
            else:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
