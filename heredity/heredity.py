import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    people_probability = dict()
    for person in people:
        people_probability[person] = dict()
        people_probability[person]["no_gene"] = 1
        people_probability[person]["one_gene"] = 1
        people_probability[person]["two_genes"] = 1
        people_probability[person]["have_trait"] = 1
        people_probability[person]["not_have_trait"] = 1

    # everyone in set `one_gene` has one copy of the gene, and
    for person in one_gene:
        if not people[person]["mother"] and not people[person]["father"]:
            people_probability[person]["one_gene"] = PROBS["gene"][1]
        else:
            if people[person]["mother"] in one_gene:
                mother_pass_probability = mother_not_pass_probability = (1-PROBS["mutation"]) / 2
            elif people[person]["mother"] in two_genes:
                mother_pass_probability = 1 - PROBS["mutation"]
                mother_not_pass_probability = PROBS["mutation"]
            else:
                mother_pass_probability = PROBS["mutation"]
                mother_not_pass_probability = 1 - PROBS["mutation"]

            if people[person]["father"] in one_gene:
                father_pass_probability = father_not_pass_probability = (1-PROBS["mutation"]) / 2
            elif people[person]["father"] in two_genes:
                father_pass_probability = 1 - PROBS["mutation"]
                father_not_pass_probability = PROBS["mutation"]
            else:
                father_pass_probability = PROBS["mutation"]
                father_not_pass_probability = 1 - PROBS["mutation"]

            people_probability[person]["one_gene"] = (mother_pass_probability * father_not_pass_probability +
                                                      father_pass_probability * mother_not_pass_probability)

    # everyone in set `two_genes` has two copies of the gene, and
    for person in two_genes:
        if not people[person]["mother"] and not people[person]["father"]:
            people_probability[person]["two_genes"] = PROBS["gene"][2]
        else:
            if people[person]["mother"] in one_gene:
                mother_pass_probability = (1 - PROBS["mutation"]) / 2
            elif people[person]["mother"] in two_genes:
                mother_pass_probability = 1 - PROBS["mutation"]
            else:
                mother_pass_probability = PROBS["mutation"]

            if people[person]["father"] in one_gene:
                father_pass_probability = (1-PROBS["mutation"]) / 2
            elif people[person]["father"] in two_genes:
                father_pass_probability = 1 - PROBS["mutation"]
            else:
                father_pass_probability = PROBS["mutation"]

            people_probability[person]["two_genes"] = mother_pass_probability * father_pass_probability

    # everyone not in `one_gene` or `two_gene` does not have the gene, and
    for person in set(people) - one_gene - two_genes:
        if not people[person]["mother"] and not people[person]["father"]:
            people_probability[person]["no_gene"] = PROBS["gene"][0]
        else:
            if people[person]["mother"] in one_gene:
                mother_not_pass_probability = (1 - PROBS["mutation"]) / 2
            elif people[person]["mother"] in two_genes:
                mother_not_pass_probability = PROBS["mutation"]
            else:
                mother_not_pass_probability = 1 - PROBS["mutation"]

            if people[person]["father"] in one_gene:
                father_not_pass_probability = (1 - PROBS["mutation"]) / 2
            elif people[person]["father"] in two_genes:
                father_not_pass_probability = PROBS["mutation"]
            else:
                father_not_pass_probability = 1 - PROBS["mutation"]

            people_probability[person]["no_gene"] = mother_not_pass_probability * father_not_pass_probability

    # everyone in set `have_trait` has the trait, and
    for person in have_trait:
        if people_probability[person]["no_gene"] != 1:
            people_probability[person]["have_trait"] = PROBS["trait"][0][True]
        elif people_probability[person]["one_gene"] != 1:
            people_probability[person]["have_trait"] = PROBS["trait"][1][True]
        else:
            people_probability[person]["have_trait"] = PROBS["trait"][2][True]

    # everyone not in set` have_trait` does not have the trait.
    for person in set(people) - have_trait:
        if people_probability[person]["no_gene"] != 1:
            people_probability[person]["not_have_trait"] = PROBS["trait"][0][False]
        elif people_probability[person]["one_gene"] != 1:
            people_probability[person]["not_have_trait"] = PROBS["trait"][1][False]
        else:
            people_probability[person]["not_have_trait"] = PROBS["trait"][2][False]

    result = 1
    for person in people:
        result *= (people_probability[person]["no_gene"] *
                   people_probability[person]["one_gene"] *
                   people_probability[person]["two_genes"] *
                   people_probability[person]["have_trait"] *
                   people_probability[person]["not_have_trait"])

    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p
        else:
            if person in one_gene:
                probabilities[person]["gene"][1] += p

            if person in two_genes:
                probabilities[person]["gene"][2] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # raise NotImplementedError
    for person in probabilities:
        for distribution in probabilities[person]:
            distributions_sum = sum(probabilities[person][distribution].values())
            for key in probabilities[person][distribution]:
                probabilities[person][distribution][key] /= distributions_sum


if __name__ == "__main__":
    main()
