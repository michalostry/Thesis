# List of configuration dictionaries
configurations = [
    {
        'num_iterations': 1,
        'num_students': 1000,
        'num_schools': 20,
        'grid_size': 5000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'debug_ids': [],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': 1
    },
    {
        'num_iterations': 1,
        'num_students': 1000,
        'num_schools': 20,
        'grid_size': 5000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'linear_decreasing',
        'debug_ids': [],  # empty for no debug
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': 2
    },
    # Add more configurations as needed
]