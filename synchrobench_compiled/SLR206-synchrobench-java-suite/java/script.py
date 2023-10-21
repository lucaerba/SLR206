import subprocess
import re

# Define the list of threads, update ratios, and list sizes
threads = [1, 4, 6, 8, 10, 12]
update_ratios = [0, 10, 100]
list_sizes = [100, 1000, 10000]

# Specify the duration in milliseconds
duration = 2000

# Specify the range multiplier
range_multiplier = 2

# Specify the synchrobench Java classpath
classpath = "bin"

# Specify the output XML file
output_file = "benchmark_results.xml"

# List of algorithms to benchmark
#
algorithms = [
    "linkedlists.lockbased.CoarseGrainedListBasedSet",
    "linkedlists.lockbased.HandOverHandListBasedSet",
    "linkedlists.lockbased.LazyLinkedListSortedSet"
]

# Create the XML file with the root element
with open(output_file, 'w') as xml_file:
    xml_file.write("<benchmark_results>\n")

    # Loop through each algorithm
    for algorithm in algorithms:
        # Loop through each combination of parameters
        for thread in threads:
            for update_ratio in update_ratios:
                for list_size in list_sizes:
                    # Calculate the range based on the multiplier
                    range_val = list_size * range_multiplier

                    # Run synchrobench with the specified parameters
                    command = f"java -cp {classpath} contention.benchmark.Test -b {algorithm} -W 0 -d {duration} -t {thread} -u {update_ratio} -i {list_size} -r {range_val}"

                    print(f"Running command: {command}")

                    # Capture the output of the command
                    result = subprocess.check_output(command, shell=True, text=True)

                    # Use regex to extract the throughput value
                    throughput_match = re.search(r'Throughput \(ops/s\):\s*([\d.]+)', result)
                    if throughput_match:
                        throughput = throughput_match.group(1)
                    else:
                        throughput = "N/A"

                    # Write the relevant output to the XML file
                    xml_file.write("  <result>\n")
                    xml_file.write(f"    <algorithm>{algorithm}</algorithm>\n")
                    xml_file.write(f"    <write_ratio>{update_ratio}%</write_ratio>\n")
                    xml_file.write(f"    <threads>{thread}</threads>\n")
                    xml_file.write(f"    <size>{list_size}</size>\n")
                    xml_file.write(f"    <throughput>{throughput}</throughput>\n")
                    xml_file.write("  </result>\n")

                    print("-------------------------------------------")
    # Close the XML file with the root element
    xml_file.write("</benchmark_results>\n")

print(f"Results saved to {output_file}")


#3 + 3 + 1 plot

#3 ( one per algorithm) -> each one 3 curves (for lists sizes), u=10      y=throughput x=threads
#3 ( one per algorithm) -> each one 3 curves (for 3 -u ), -l=100      y=throughput x=threads
#1 ->  3 curves (for 3 algorithm), -l=1000 -u=10    y=throughput x=threads
