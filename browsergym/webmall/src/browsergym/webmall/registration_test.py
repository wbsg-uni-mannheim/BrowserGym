# registration_test.py
import browsergym.webmall  # This will trigger the task registration process

# Check if tasks are properly registered in Gym registry
import gymnasium as gym

# List all the environments in the registry, to see if your WebMall tasks appear
print("Registered environments:", gym.envs.registry)

# Optionally, check if a specific task is registered
# Replace `Webmall_Single_Product_Search_Task1` with the actual task name you're expecting to see
try:
    env = gym.make('browsergym/webmall.Webmall_Single_Product_Search_Task1')  # Example task name
    print(f"Environment {env} has been registered successfully.")
    print(gym.envs.registry.keys())
except Exception as e:
    print(f"Error: {e}")