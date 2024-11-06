#!/bin/bash

# Run this script as is to monitor all running containers on the host machine.
# Run this script with "-c <container-name-filter>" to filter running containers that contain a specified substring in their names.

while getopts ":c:" opt; do
  case $opt in
    c) container_name_filter="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

echo "Starting Docker container resource monitoring"
if [ -n "$container_name_filter" ]; then
  echo "Only monitoring running containers that contain '$container_name_filter' in their names"
fi

# Create a timestamp for the output file
time_file=$(date '+%Y%m%d-%H%M%S')
# Set the name of the output file to write to
out_file_name="resource-monitor-docker-$time_file.csv"
# Write the first line of the output CSV, i.e. the names of the columns
echo "Time,Container name,CPU usage,Memory usage, Memory limit" >> $out_file_name

echo "Monitoring has started!"

# Start an infinite execution loop that only stops if the user wishes to
while true; do
  # Get all running pods in the K8s cluster
  stats=$(docker stats --format "{{.Name}} {{.CPUPerc}} {{.MemUsage}}" --no-stream)

  while IFS= read -r line; do
    container_name=$(echo $line | awk '{print $1}')

    # If filter is active, only poll from pods that contain the filter substring
    if [[ -z "$container_name_filter" || -n "$container_name_filter" && "$container_name" == *"$container_name_filter"* ]]; then
      # Record the time at which the pod is last polled from
      time_row=$(date '+%Y-%m-%d %H:%M:%S')

      # This is used instead of "kubectl top pod" to reduce delays between pod start-up and polling
      # "kubectl top pod" takes around a minute after pod start-up before it can start polling
      cpu_value=$(echo $line | awk '{print $2}')
      mem_usage_value=$(echo $line | awk '{print $3}')
      mem_limit_value=$(echo $line | awk '{print $5}')

      # Write a new row to the output CSV
      echo "$time_row,$container_name,$cpu_value,$mem_usage_value,$mem_limit_value" >> $out_file_name
      
      # Print the same output to the user via the Bash terminal
      echo "$time_row: $container_name $cpu_value $mem_usage_value $mem_limit_value"
    fi
  done <<< "$stats"

  # Wait before starting the next round of polling
  sleep 0.5
done