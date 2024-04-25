import pandas as pd
import matplotlib.pyplot as plt
import os

# Load datasets
df_algo1 = pd.read_csv("results_additive_increment.csv")
df_algo2 = pd.read_csv("results_multiplicative_increment.csv")

# Create a folder to save plots if it doesn't exist
output_folder = "plots"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to plot comparison graphs with PCN configurations as x-axis
def plot_comparison(df1, df2, x_column, y_column, x_label, y_label, title, filename, show_average=True):
    plt.figure(figsize=(10, 6))
    
    # Plot data for Additive_Algorithm
    if not df1.empty:
        plt.plot(df1[x_column], df1[y_column], label='Additive_Algorithm')
        if show_average:
            avg_algo1 = df1[y_column].mean()
            plt.axhline(y=avg_algo1, color='red', linestyle='--', label='Average Additive_Algorithm')
    
    # Plot data for Multiplicative_Algorithm
    if not df2.empty:
        plt.plot(df2[x_column], df2[y_column], label='Multiplicative_Algorithm')
        if show_average:
            avg_algo2 = df2[y_column].mean()
            plt.axhline(y=avg_algo2, color='blue', linestyle='--', label='Average Multiplicative_Algorithm')
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, filename))
    plt.show()

# Function to plot scatter plot
def scatter_plot(df1, df2, x_column, y_column, x_label, y_label, title, filename):
    plt.figure(figsize=(10, 6))
    plt.scatter(df1[x_column], df1[y_column], label='Additive_Algorithm')
    plt.scatter(df2[x_column], df2[y_column], label='Multiplicative_Algorithm')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, filename))
    plt.show()

# Function to plot bar plot
def bar_plot(df1, df2, x_column, y_column, x_label, y_label, title, filename):
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = sorted(list(set(df_algo1[x_column].unique()) | set(df_algo2[x_column].unique())))
    plt.bar(index, df1.groupby(x_column)[y_column].mean().reindex(index), bar_width, label='Additive_Algorithm')
    plt.bar([i + bar_width for i in index], df2.groupby(x_column)[y_column].mean().reindex(index), bar_width, label='Multiplicative_Algorithm')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, filename))
    plt.show()

# Function to plot histogram
def histogram_plot(df1, df2, column, x_label, y_label, title, filename):
    plt.figure(figsize=(10, 6))
    plt.hist(df1[column], bins=20, alpha=0.5, label='Additive_Algorithm', color='blue')
    plt.hist(df2[column], bins=20, alpha=0.5, label='Multiplicative_Algorithm', color='orange')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, filename))
    plt.show()

# Function to plot box plot
def box_plot(df1, df2, x_column, y_column, x_label, y_label, title, filename):
    plt.figure(figsize=(10, 6))
    plt.boxplot([df1[y_column], df2[y_column]], labels=['Additive_Algorithm', 'Multiplicative_Algorithm'])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, filename))
    plt.show()

# Compare total bidding vs. number of nodes
plot_comparison(df_algo1, df_algo2, 'num_nodes', 'time', 'Number of Nodes', 'Time', 'Time vs Number of Nodes', 'time_vs_number_of_nodes.png',show_average=True)

# Compare total bidding vs. number of edges
plot_comparison(df_algo1, df_algo2, 'num_edges', 'time', 'Number of Edges', 'Time', 'Time vs Number of Edges', 'time_vs_number_of_edges.png',show_average=True)

# Compare total bidding vs. number of nodes
plot_comparison(df_algo1, df_algo2, 'num_nodes', 'total_bidding', 'Number of Nodes', 'Total Bidding', 'Total Bidding vs Number of Nodes', 'total_bidding_vs_number_of_nodes.png',show_average=False)

# Compare total bidding vs. number of edges
plot_comparison(df_algo1, df_algo2, 'num_edges', 'total_bidding', 'Number of Edges', 'Total Bidding', 'Total Bidding vs Number of Edges', 'total_bidding_vs_number_of_edges.png',show_average=False)

# Compare total outsourcing vs. number of nodes
plot_comparison(df_algo1, df_algo2, 'num_nodes', 'total_outsourcing', 'Number of Nodes', 'Total Outsourcing', 'Total Outsourcing vs Number of Nodes', 'total_outsourcing_vs_number_of_nodes.png',show_average=False)

# Compare total outsourcing vs. number of edges
plot_comparison(df_algo1, df_algo2, 'num_edges', 'total_outsourcing', 'Number of Edges', 'Total Outsourcing', 'Total Outsourcing vs Number of Edges', 'total_outsourcing_vs_number_of_edges.png',show_average=False)

# Compare probability updates vs. number of nodes
plot_comparison(df_algo1, df_algo2, 'num_nodes', 'propability_updates', 'Number of Nodes', 'Probability Updates', 'Probability Updates vs Number of Nodes', 'probability_updates_vs_number_of_nodes.png',show_average=True)

# Compare probability updates vs. number of edges
plot_comparison(df_algo1, df_algo2, 'num_edges', 'propability_updates', 'Number of Edges', 'Probability Updates', 'Probability Updates vs Number of Edges', 'probability_updates_vs_number_of_edges.png',show_average=True)

# Scatter plot: Total Bidding vs. Total Outsourcing
scatter_plot(df_algo1, df_algo2, 'total_bidding', 'total_outsourcing', 'Total Bidding', 'Total Outsourcing', 'Total Bidding vs Total Outsourcing', 'total_bidding_vs_total_outsourcing.png')

# Bar plot: Average Total Bidding by Number of Nodes
bar_plot(df_algo1, df_algo2, 'num_nodes', 'total_bidding', 'Number of Nodes', 'Average Total Bidding', 'Average Total Bidding by Number of Nodes', 'average_total_bidding_by_num_nodes.png')

# Histogram: Distribution of Probability Updates
histogram_plot(df_algo1, df_algo2, 'propability_updates', 'Probability Updates', 'Frequency', 'Distribution of Probability Updates', 'distribution_of_probability_updates.png')

# Box plot: Failed Transactions Distribution
box_plot(df_algo1, df_algo2, None, 'failed_transactions', None, 'Failed Transactions', 'Failed Transactions Distribution', 'failed_transactions_distribution.png')
