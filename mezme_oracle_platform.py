from mezme_agent import MezmeAgent
import json

class CryptoOraclePlatform:
    def __init__(self):
        self.deployed_agents = {}

    def deploy_agent(self, agent_name, agent_config):
        """Deploy a new Mezme agent with the given configuration."""
        if agent_name in self.deployed_agents:
            raise ValueError(f"Agent with name '{agent_name}' already exists.")
        
        # Create and initialize the new agent
        agent = MezmeAgent(agent_config)
        self.deployed_agents[agent_name] = agent
        print(f"Agent '{agent_name}' deployed successfully!")
        return agent_name

    def run_agent(self, agent_name, data):
        """Run an agent with the provided data."""
        if agent_name not in self.deployed_agents:
            raise ValueError(f"No agent named '{agent_name}' found.")
        
        agent = self.deployed_agents[agent_name]
        return agent.process_data(data)

    def get_agent_info(self, agent_name):
        """Retrieve information about a deployed agent."""
        if agent_name not in self.deployed_agents:
            return None
        agent = self.deployed_agents[agent_name]
        return {
            "name": agent_name,
            "model": agent.model_type,
            "features": agent.features,
            "threshold": agent.threshold
        }

    def list_agents(self):
        """List all deployed agents with basic info."""
        return {name: self.get_agent_info(name) for name in self.deployed_agents}

    def delete_agent(self, agent_name):
        """Remove an agent from the platform."""
        if agent_name in self.deployed_agents:
            del self.deployed_agents[agent_name]
            print(f"Agent '{agent_name}' has been deleted.")
        else:
            print(f"No agent named '{agent_name}' found to delete.")

if __name__ == "__main__":
    platform = CryptoOraclePlatform()
    # Example usage:
    config = {
        "model_type": "RandomForest",
        "features": ["temperature", "humidity"],
        "threshold": 0.5  # Example threshold for some decision or alert
    }
    platform.deploy_agent("weather_analyzer", config)
    print(platform.list_agents())
