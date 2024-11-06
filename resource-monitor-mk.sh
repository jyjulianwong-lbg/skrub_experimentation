#!/bin/bash

# Run this script as is to monitor all running pods cluster-wide.
# Run this script with "-p <pod-name-filter>" to filter running pods that contain a specified substring in their names.

while getopts ":p:" opt; do
  case $opt in
    p) pod_name_filter="$OPTARG"
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

echo "Starting cluster-wide K8s Metrics Server monitoring"
if [ -n "$pod_name_filter" ]; then
  echo "Only monitoring running pods that contain '$pod_name_filter' in their names"
fi

# Create a timestamp for the output file
time_file=$(date '+%Y%m%d-%H%M%S')
# Set the name of the output file to write to
out_file_name="resource-monitor-mk-$time_file.csv"
# Write the first line of the output CSV, i.e. the names of the columns
echo "Time,Pod name,CPU usage (nanoseconds),Memory usage (bytes)" >> $out_file_name

echo "Monitoring has started!"

# Start an infinite execution loop that only stops if the user wishes to
while true; do
  # Get all running pods in the K8s cluster
  pod_names=$(kubectl get pods --field-selector=status.phase=Running --no-headers | awk '{print $1}')

  while IFS= read -r line; do
    pod_name=$line
    if [[ -z "$pod_name" ]]; then
      # Delete the previous output line, which will be "No resources found..." from kubectl
      printf '\033[1A\033[K'
      break
    fi

    # If filter is active, only poll from pods that contain the filter substring
    if [[ -z "$pod_name_filter" || -n "$pod_name_filter" && "$pod_name" == *"$pod_name_filter"* ]]; then
      # Record the time at which the pod is last polled from
      time_row=$(date '+%Y-%m-%d %H:%M:%S')

      # This is used instead of "kubectl top pod" to reduce delays between pod start-up and polling
      # "kubectl top pod" takes around a minute after pod start-up before it can start polling
      # TODO: To convert cpu_value (in nanoseconds) to millicores (i.e. the value that appears in the K8s manifest), 
      # take the difference between the current value and the last value, dV, 
      # take the difference in time between the current timestamp and the last timestamp, dT, 
      # and calculate dV / (dT * 10^6). 
      # This is not calculcated here because Bash cannot handle floating point division. 
      # I'm sorry. 
      cpu_value=$(kubectl exec $pod_name -- cat //sys/fs/cgroup/cpuacct/cpuacct.usage)
      # TODO: To convert ram_value (in bytes) to MB (megabytes), divide by 10^6. 
      ram_value=$(kubectl exec $pod_name -- cat //sys/fs/cgroup/memory/memory.usage_in_bytes)

      # Write a new row to the output CSV
      echo "$time_row,$pod_name,$cpu_value,$ram_value" >> $out_file_name
      
      # Print the same output to the user via the Bash terminal
      echo -e "$time_row: $pod_name\t$cpu_value\t$ram_value"
    fi
  done <<< "$pod_names"

  # Wait before starting the next round of polling
  sleep 0.5
done