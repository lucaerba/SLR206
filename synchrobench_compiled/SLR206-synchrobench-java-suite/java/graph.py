import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
import os

# Create a directory for saving plots
if not os.path.exists("plots"):
    os.makedirs("plots")

# Parse the XML data
tree = ET.parse('benchmark_results.xml')
root = tree.getroot()

# Initialize data structures to store parsed data
data = []

# Iterate through the XML data and extract relevant information
for result in root.findall('.//result'):
    algorithm = result.find('algorithm').text
    write_ratio = result.find('write_ratio').text
    threads = int(result.find('threads').text)
    list_size = int(result.find('size').text)
    throughput = float(result.find('throughput').text)

    data.append({
        'Algorithm': algorithm,
        'Write Ratio': write_ratio,
        'Threads': threads,
        'List Size': list_size,
        'Throughput': throughput
    })

# Convert data to a DataFrame for easier manipulation
df = pd.DataFrame(data)

# Create subplots for each algorithm
algorithms = df['Algorithm'].unique()

# Plot 1: Three curves for each algorithm with fixed u=10 and varying list sizes
for i, algorithm in enumerate(algorithms):
    plt.figure(figsize=(15, 5))
    for list_size in [100, 1000, 10000]:
        subset = df[(df['Algorithm'] == algorithm) & (df['Write Ratio'] == '10%') & (df['List Size'] == list_size)]
        plt.plot(subset['Threads'], subset['Throughput'], label=f'List Size {list_size}')
    plt.xlabel('Threads')
    plt.ylabel('Throughput')
    #plt.yscale('log')  # Set the y-axis to log scale
    plt.title(f'{algorithm.split(".")[2]} - Update Ratio 10%')
    plt.legend()
    plt.grid(True)  # Add grid lines
    plt.savefig(f'plots/{algorithm.split(".")[2]}_u10.png')  # Save the plot as an image

# Plot 2: Three curves for each algorithm with fixed list size=100 and varying u values
for i, algorithm in enumerate(algorithms):
    plt.figure(figsize=(15, 5))
    for write_ratio in [0, 10, 100]:
        subset = df[(df['Algorithm'] == algorithm) & (df['Write Ratio'] == f'{write_ratio}%') & (df['List Size'] == 100)]
        plt.plot(subset['Threads'], subset['Throughput'], label=f'Update Ratio={write_ratio}%')
    plt.xlabel('Threads')
    plt.ylabel('Throughput')
    #plt.yscale('log')  # Set the y-axis to log scale
    plt.title(f'{algorithm.split(".")[2]} - List Size 100')
    plt.legend()
    plt.grid(True)  # Add grid lines
    plt.savefig(f'plots/{algorithm.split(".")[2]}_list100.png')  # Save the plot as an image

# Plot 3: Single plot with three curves for each algorithm with fixed list size=1000 and u=10%
plt.figure(figsize=(10, 5))
for algorithm in algorithms:
    subset = df[(df['Algorithm'] == algorithm) & (df['Write Ratio'] == '10%') & (df['List Size'] == 1000)]
    plt.plot(subset['Threads'], subset['Throughput'], label=algorithm.split(".")[2])

plt.xlabel('Threads')
plt.ylabel('Throughput')
#plt.yscale('log')  # Set the y-axis to log scale
plt.title('List Size 1000 - Update Ratio 10%')
plt.legend()
plt.grid(True)  # Add grid lines
plt.savefig('plots/list1000_u10.png')  # Save the plot as an image

# Close any open plots
plt.close('all')
