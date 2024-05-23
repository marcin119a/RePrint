import numpy as np
import pandas as pd

data = {
    'signaturesCOSMIC.csv': [x for x in range(1, 31) ],
    'WGS_signatures__sigProfiler_SBS_signatures_2019_05_22.modified.csv': [x for x in range(0, 64)],
    'COSMIC_v1_SBS_GRCh37.txt': [1, 2, 3, 4, 5, 6, 7, 9, 15],
    'COSMIC_v2_SBS_GRCh37.txt': [1, 2, 3, 5, 6, 8, 13, 17, 18, 20, 26, 30],
    'COSMIC_v3.1_SBS_GRCh37.txt': [1, 2, 3, 5, 6, 8, 13, 17, 18, 20, 26, 30],
}

def calculate_rmse(x, y):
    return np.sqrt(np.nanmean((x - y) ** 2))

def calculate_cosine(x, y):
    return -np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

def reprint(data, epsilon=10e-4):
    # Extracting mutation categories and their probabilities
    mutation_types = data.index
    signatures = data.columns[1:]

    # Initialize a dictionary to store the RePrint probabilities for each signature
    reprint_probabilities = {signature: {} for signature in signatures}

    # Iterate over each signature
    for signature in signatures:
        # Extract the probabilities for the current signature
        signature_probs = data[signature].values + epsilon

        # Iterate over each mutation type
        for idx, mutation in enumerate(mutation_types):
            # Split the mutation type to extract NL, X, Y, NR
            NL = mutation[0]
            NR = mutation[6]
            X, Y = mutation[2], mutation[4]

            # Compute the denominator: sum of probabilities for Z != X
            denominator = np.sum([signature_probs[j] for j in range(len(mutation_types))
                                  if mutation_types[j].startswith(f"{NL}[{X}>") and mutation_types[j].endswith(f"]{NR}")
                                  and mutation_types[j][4] != X])

            # Compute the RePrint probability for the current mutation
            reprint_prob = signature_probs[idx] / denominator if denominator != 0 else 0

            # Store the RePrint probability
            reprint_probabilities[signature][mutation] = reprint_prob

    # Convert the reprint_probabilities dictionary to a DataFrame for better readability
    reprint_df = pd.DataFrame(reprint_probabilities)
    return reprint_df