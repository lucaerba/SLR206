#!/bin/bash

# Define the list of threads, update ratios, and list sizes
threads=(1 4 6 8 10 12)
update_ratios=(0 10 100)
list_sizes=(100 1000 10000)

# Specify the duration in milliseconds
duration=2000

# Specify the range multiplier
range_multiplier=2

# Specify the synchrobench Java classpath
classpath="bin"

# Specify the output XML file
output_file="benchmark_results.xml"

# List of algorithms to benchmark
algorithms=("linkedlists.lockbased.CoarseGrainedListBasedSet" "linkedlists.lockbased.HandOverHandListBasedSet" "linkedlists.lockbased.LazyLinkedListBasedSet")

# Create the XML file with the root element
echo "<benchmark_results>" > "$output_file"

# Loop through each algorithm
for algorithm in "${algorithms[@]}"; do
  # Loop through each combination of parameters
  for thread in "${threads[@]}"; do
    for update_ratio in "${update_ratios[@]}"; do
      for list_size in "${list_sizes[@]}"; do
        # Calculate the range based on the multiplier
        range=$((list_size * range_multiplier))

        # Run synchrobench with the specified parameters
        command="java -cp $classpath contention.benchmark.Test -b $algorithm -W 0 -d $duration -t $thread -u $update_ratio -i $list_size -r $range"

        echo "Running command: $command"

        # Capture the throughput variable
        result=$($command)
        throughput=$(echo "$result" | grep -oP 'Throughput \(ops/s\): \K.*')


        # Write the relevant output to the XML file
        echo "  <result>" >> "$output_file"
        echo "    <algorithm>$algorithm</algorithm>" >> "$output_file"
        echo "    <write_ratio>$update_ratio%</write_ratio>" >> "$output_file"
        echo "    <threads>$thread</threads>" >> "$output_file"
        echo "    <size>$list_size</size>" >> "$output_file"
        echo "    <throughput>$throughput</throughput>" >> "$output_file"
        echo "  </result>" >> "$output_file"

        echo "-------------------------------------------"
      done
    done
  done
done

# Close the XML file with the root element
echo "</benchmark_results>" >> "$output_file"

