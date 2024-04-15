import argparse
import os
import time
import torch

class Config:
    # Run a smaller config on your local machine
    local_mode = False  # Run in local mode
    # Track to run - options: reinforcement_learning, curriculum_generation
    track = "rl"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #record_loss = False  # log all minibatch loss and actions, for debugging

    # Trainer Args
    seed = 1
    num_cores = None  # Number of cores to use for training
    num_envs = 6  # Number of environments to use for training
    num_buffers = 2  # Number of buffers to use for training
    rollout_batch_size = 2**15 # Number of steps to rollout
    eval_batch_size = 2**15 # Number of steps to rollout for eval
    train_num_steps = 10_000_000  # Number of steps to train
    eval_num_steps = 1_000_000  # Number of steps to evaluate
    checkpoint_interval = 30  # Interval to save models
    run_name = f"nmmo_{time.strftime('%Y%m%d_%H%M%S')}"  # Run name
    runs_dir = "/tmp/runs"  # Directory for runs
    policy_store_dir = None # Policy store directory
    use_serial_vecenv = False  # Use serial vecenv implementation
    learner_weight = 1.0  # Weight of learner policy
    max_opponent_policies = 0  # Maximum number of opponent policies to train against
    eval_num_policies = 2 # Number of policies to use for evaluation
    eval_num_rounds = 1 # Number of rounds to use for evaluation
    wandb_project = None  # WandB project name
    wandb_entity = None  # WandB entity name

    # PPO Args
    bptt_horizon = 8  # Train on this number of steps of a rollout at a time. Used to reduce GPU memory.
    ppo_training_batch_size = 128  # Number of rows in a training batch
    ppo_update_epochs = 3  # Number of update epochs to use for training
    ppo_learning_rate = 0.00015  # Learning rate
    clip_coef = 0.1  # PPO clip coefficient

    # Environment Args
    num_agents = 128  # Number of agents to use for training
    num_npcs = 256  # Number of NPCs to use for training
    max_episode_length = 1024  # Number of steps per episode
    death_fog_tick = None  # Number of ticks before death fog starts
    num_maps = 128  # Number of maps to use for training
    maps_path = "maps/train/"  # Path to maps to use for training
    map_size = 128  # Size of maps to use for training
    resilient_population = 0.2  # Percentage of agents to be resilient to starvation/dehydration
    tasks_path = None  # Path to tasks to use for training
    eval_mode = False # Run the postprocessor in the eval mode
    early_stop_agent_num = 8  # Stop the episode when the number of agents reaches this number
    sqrt_achievement_rewards=False # Use the log of achievement rewards
    heal_bonus_weight = 0.03
    meander_bonus_weight = 0.02
    explore_bonus_weight = 0.01
    spawn_immunity = 20

    # Policy Args
    input_size = 256
    hidden_size = 256
    num_lstm_layers = 0  # Number of LSTM layers to use
    task_size = 4096  # Size of task embedding
    encode_task = True  # Encode task
    attend_task = "none"  # Attend task - options: none, pytorch, nikhil
    attentional_decode = True  # Use attentional action decoder
    extra_encoders = True  # Use inventory and market encoders

    @classmethod
    def asdict(cls):
        return {attr: getattr(cls, attr) for attr in dir(cls)
                if not callable(getattr(cls, attr)) and not attr.startswith("__")}

def create_config(config_cls):
    parser = argparse.ArgumentParser()

    # Get attribute names and their values from the static class
    attrs = config_cls.asdict()

    # Iterate over these attributes and set the default values of arguments to the corresponding attribute values
    for attr, value in attrs.items():
        # Convert underscores to hyphens to match the argparse argument format
        arg_name = f'--{attr.replace("_", "-")}'

        parser.add_argument(
            arg_name,
            dest=attr,
            type=type(value) if value is not None else str,
            default=value,
            help=f"{arg_name} (default: {value})"
        )

    return parser.parse_args()
