from autora.experimentalist.example_experimentalist import sample
import numpy as np

# Note: We encourage you to write more functionality tests for your sampler.

def test_output_dimensions():
    conditions = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    n = 2
    conditions_new = sample(conditions, n)

    # Check that the sampler returns n experimental conditions
    assert conditions_new.shape == (n, conditions.shape[1])
