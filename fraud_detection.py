# Scarlett Nguyen
import utils  # noqa: F401, do not remove if using a Mac
# add your imports BELOW this line
import matplotlib.pyplot as plt
import random
import csv


# Your Set of Functions for this assignment goes in here
# Problem 1: Read and clean Iranian election data
def extract_election_vote_counts(filename, column_names):
    open_csv = open(filename)
    input_file = csv.DictReader(open_csv)

    output_list = []
    for rows in input_file:
        for name in column_names:
            if rows[name] != "":
                num_votes = rows[name].replace(",", "")
                output_list.append(int(num_votes))
    return output_list
    open_csv.close()


# Problem 2: Make a histogram
def ones_and_tens_digit_histogram(numbers):
    output_list = []
    for i in range(10):
        output_list.append(0)
    for number in numbers:
        one_digit = number % 10
        ten_digit = (number // 10) % 10
        output_list[one_digit] += 1
        output_list[ten_digit] += 1
    for i in range(10):
        output_list[i] /= len(numbers) * 2
    return output_list


# Problem 3: Plot election data
def plot_iran_least_digits_histogram(histogram):
    x_axis = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ideal_line = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    plt.plot(x_axis, ideal_line, color='blue', label="ideal")
    plt.plot(x_axis, histogram, color='orange', label="iran")
    plt.xlabel("Digit")
    plt.ylabel("Frequency")
    plt.title("Distribution of The Last Two Digits in Iranian Dataset")
    plt.legend(loc="upper left")

    plt.savefig("iran-digits.png")
    plt.clf()


# Problem 4: Plot smaller samples
# Notes: Smaller samples have more variation.
def plot_distribution_by_sample_size():
    plt.clf()
    x_axis = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ideal_line = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    sample_size = [10, 50, 100, 1000, 10000]
    sample_dict = {}

    plt.plot(x_axis, ideal_line, color="blue", label="ideal")
    for number in sample_size:
        y_axis = get_sample(number)
        sample_dict[number] = ones_and_tens_digit_histogram(y_axis)

    for item in sample_dict.items():
        plt.plot(x_axis, item[1], label=str(item[0]) + " random numbers")
        plt.xlabel("Digit")
        plt.ylabel("Frequency")
        plt.title("Distribution of The Last Two Digits in Iranian Dataset")
        plt.legend(loc="upper left")

        plt.savefig("random-digits.png")
        plt.clf()


# Problem 5: Comparing variation of samples
def mean_squared_error(numbers1, numbers2):
    sum_var = 0
    for i in range(len(numbers1)):
        sum_var += (numbers1[i] - numbers2[i]) ** 2
    return sum_var / len(numbers1)


# Problem 6: Comparing variation of samples
# 6.1:
# Take a histogram (as created by ones_and_tens_digit_histogram)
# Return the mean squared error of the given histogram with the uniform distribution
def calculate_mse_with_uniform(histogram):
    uniform_dist = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    return mean_squared_error(histogram, uniform_dist)


# get list of groups of given sample size
def get_sample_groups(size):
    samples = []
    for index in range(10000):
        samples.append(get_sample(size))
    return samples


# get a list of random numbers 0 to 99
def get_sample(size):
    arr = []
    for item in range(size):
            arr.append(random.randint(0, 99))
    return arr


# return number of mse greater than given mse
def greater_mse(groups, test_mse):
    greater_equal = 0
    for group in groups:
        histogram = ones_and_tens_digit_histogram(group)
        mse = calculate_mse_with_uniform(histogram)
        if (mse >= test_mse):
            greater_equal += 1
    return greater_equal


# 6.2:
# Compare Iran MSEs to samples
def compare_iran_mse_to_samples(iran_mse, number_of_iran_samples):
    groups = get_sample_groups(number_of_iran_samples)
    greater_equal = greater_mse(groups, iran_mse)
    print("2009 Iranian election MSE:", iran_mse)
    print("Quantity of MSEs larger than or equal to the 2009 Iranian election MSE:", greater_equal)
    print("Quantity of MSEs smaller than the 2009 Iranian election MSE:", 10000 - greater_equal)
    print("2009 Iranian election null hypothesis rejection level p:", greater_equal / 10000)


# Compares US election MSE to MSEs of randomly generated samples
def compare_us_mse_to_samples(us_mse, number_of_us_samples):
    groups = get_sample_groups(number_of_us_samples)
    greater_equal = greater_mse(groups, us_mse)
    print("2008 United States election MSE:", us_mse)
    print("Quantity of MSEs larger than or equal to the 2008 United States election MSE:", greater_equal)
    print("Quantity of MSEs smaller than the 2008 United States election MSE:", 10000 - greater_equal)
    print("2008 United States election null hypothesis rejection level p:", greater_equal / 10000)


# The code in this function is executed when this file is run as a Python program
def main():
    # Code that calls functions you have written above
    # e.g. extract_election_vote_counts() etc.
    # This code should produce the output expected from your program.
    iran_file = "election-iran-2009.csv"
    iran_col_names = ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"]

    us_file = "election-us-2008.csv"
    us_col_names = ["Obama", "McCain", "Nader", "Barr", "Baldwin", "McKinney"]

    # Iran's election
    # P1
    iran_vote_list = extract_election_vote_counts(iran_file, iran_col_names)

    # P2
    iran_histogram = ones_and_tens_digit_histogram(iran_vote_list)

    # P3
    plot_iran_least_digits_histogram(iran_histogram)

    # P4
    plot_distribution_by_sample_size()

    # P6.1
    iran_mse = calculate_mse_with_uniform(iran_histogram)

    # P6.2
    compare_iran_mse_to_samples(iran_mse, len(iran_vote_list))
    print()

    # P8 2008 US election
    us_vote_list = extract_election_vote_counts(us_file, us_col_names)
    us_histogram = ones_and_tens_digit_histogram(us_vote_list)
    us_mse = calculate_mse_with_uniform(us_histogram)
    compare_us_mse_to_samples(us_mse, len(us_vote_list))


if __name__ == "__main__":
    main()
