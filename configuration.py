# List of configuration dictionaries
configurations = [
    {
        'num_iterations': 20,
        'num_students': 100,
        'num_schools': 2,
        'grid_size': 5000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'income_based_tiered_noise',
        'income_scaling_factor': 1.0,
        'debug_ids': [],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "letstry",
        'variable_to_iterate': 'income_scaling_factor',         # The variable to iterate over #'None' for no iteration
        'start_value': 0.5,                                       # Starting value for the iteration
        'increment': 0.1,                                       # Increment for each iteration
        'variable_iterations': 3                                        # Number of iterations or configurations

    },
    ]