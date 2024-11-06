# Skrub Experimentation

## How to do resource monitoring for a Reconciler K8s Job triggered from AARP

```
cd /path/to/skrub_experimentation
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

### 3. Prepare the AARP web app and the Reconciler job
Build the Reconciler Docker image and prepare the Minikube cluster.
```
cd /path/to/tnt01-aud-aarp-app-reconciler
minikube start
minikube addons enable gcp-auth
eval $(minikube -p minikube docker-env)
docker build . -t <image-name>
kubectl create namespace <namespace>
```
`<image-name>` is most likely going to be `aud-aarp-reconciler`.
`<namespace>` is most likely going to be `aud-aarp-reconciler`.

Have the AARP web app open in your web browser and be ready to trigger Reconciler. Do **not** trigger the job yet.

### 4. Set `kubectl` to the correct namespace
If the Reconciler job is being triggered in the default namespace, you can skip this step.
If not, run:
```
kubectl config set-context --current --namespace=<namespace>
```
`<namespace>` is most likely going to be `aud-aarp-reconciler`.

### 5. Start the resource monitoring script in the background
In a **separate Git Bash window**, run:
```
sh resource-monitor-mk.sh -p <pod-name>
```
`<pod-name>` is most likely going to be `aud-aarp-reconciler`.

### 6. Trigger Reconciler

### 7. View the results
Stop the background resource monitoring script by entering `CTRL-C` in the Git Bash window it is running in.
A new CSV file with a name starting with `resource-monitor-mk-...csv` will appear in the same folder where you started your resource monitoring script. Enjoy!

## How to do resource monitoring for a generic Reconciler Docker container

```
cd /path/to/skrub_experimentation
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
Stop the background resource monitoring script by entering `CTRL-C` in the Git Bash window it is running in.
A new CSV file with a name starting with `resource-monitor-docker-...csv` will appear in the same folder where you started your resource monitoring script. Enjoy!