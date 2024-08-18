# List of configuration dictionaries

# disable set seed!

configurations = [
    {
        'num_iterations': 1,
        'num_students': 30,
        'num_schools': 3,
        'grid_size': 5000,
        'weights': (0.2, 0.2, 0.2, 1),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',          #income_based_tiered_noise or constant
        'income_scaling_factor': 0.5,
        'debug_ids': [0],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "testing income_based_tiered_noise",
        'variable_to_iterate': None,         # The variable to iterate over #'None' for no iteration
        'start_value': 0.0,                                       # Starting value for the iteration
        'increment': 0.1,                                       # Increment for each iteration
        'variable_iterations': 1                                      # Number of iterations or configurations

    }
    ]