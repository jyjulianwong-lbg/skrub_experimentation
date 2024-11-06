# Skrub Experimentation

## How to do resource monitoring for any Reconciler Docker container

```
cd /path/to/skrub_experimenation
```

### 1. Install dependencies
```
pip install requirements.txt
```

### 2. Generate the sample dataset
`data_generator.py` generates 2 CSV files in the `data/` folder for the Reconciler to use.
The 2 CSV files are 2 separate datasets that share the same primary key, `Country` and `Country Name`.
The base datasets contain 100 rows each. To increase this, change `CUSTOM_AUGMENT_TIMES` at the top of the `.py` file. For example, to generate 1000 rows for each CSV file, set `CUSTOM_AUGMENT_TIMES = 10`.
To test **exact reconciliation**, comment out lines 13 to 19. To test **fuzzy reconciliation**, leave the file as is.
```
python -m data_generator
```

### 3. Build the Reconciler Docker image
```
docker build . -t <image-name>
```

### 4. Start the resource monitoring script in the background
In a **separate Git Bash window**, run:
```
sh resource-monitor-docker.sh -c <container-name>
```

### 5. Start the Reconciler Docker container
```
docker run --name <container-name> <image-name>
```

### 6. View the results
A new CSV file with a name starting with `resource-monitor-docker-...csv` will appear in the same folder where you started your resource monitoring script. Enjoy!