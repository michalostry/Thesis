# List of configuration dictionaries

# disable set seed!

configurations = [
    {
        'num_iterations': 20,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'income_based_tiered_noise',          #income_based_tiered_noise or constant
        'income_scaling_factor': 0.5,
        'debug_ids': [],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "TEST_",
        'variable_to_iterate': None,        # The variable to iterate over #'None' for no iteration
        'start_value': 0.0,                                       # Starting value for the iteration
        'increment': 0.1,                                       # Increment for each iteration
        'variable_iterations': 1                                      # Number of iterations or configurations

    },
{
        'num_iterations': 2,
        'num_students': 100,
        'num_schools': 2,
        'grid_size': 5000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',          #income_based_tiered_noise or constant
        'income_scaling_factor': 0.5,
        'debug_ids': [],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "testing constant",
        'variable_to_iterate': None,         # The variable to iterate over #'None' for no iteration
        'start_value': 0.0,                                       # Starting value for the iteration
        'increment': 0.1,                                       # Increment for each iteration
        'variable_iterations': 1                                      # Number of iterations or configurations

    }
    ]