# List of configuration dictionaries with varying Aspiration weights

configurations = [
    # 1. Aspiration 0.1
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.3, 0.3, 0.3, 0.1),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_01",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 2. Aspiration 0.2
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.2667, 0.2667, 0.2667, 0.2),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_02",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 3. Aspiration 0.3
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.2333, 0.2333, 0.2333, 0.3),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_03",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 4. Aspiration 0.4
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.2, 0.2, 0.2, 0.4),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_04",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 5. Aspiration 0.5
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.1667, 0.1667, 0.1667, 0.5),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_05",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 6. Aspiration 0.6
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.1333, 0.1333, 0.1333, 0.6),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_06",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 7. Aspiration 0.8
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.0667, 0.0667, 0.0667, 0.8),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_08",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    },
    # 8. Aspiration 0.9
    {
        'num_iterations': 500,
        'num_students': 7000,
        'num_schools': 150,
        'grid_size': 70000,
        'weights': (0.0333, 0.0333, 0.0333, 0.9),  # Distance, Quality, Income_aspiration, Aspiration
        'noise_sd': 20,
        'noise_type': 'constant',
        'income_scaling_factor': 0.5,
        'debug_ids': [],
        'school_capacity_min': 25,
        'school_capacity_max': 75,
        'config_name': "external_sensitivity_aspiration_09",
        'variable_to_iterate': 'noise_sd',
        'start_value': 20,
        'increment': 10,
        'variable_iterations': 1
    }
]
