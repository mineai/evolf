# Mine AI: Mine your AI
## We Provide an optimization framework called DEALT: Distributed Evolutionary Algorithms for Learning and Training.

## The main technologies that contribute DEALT are:
### 1) Evolf: Evolutionary Optimization for Loss Functions.
#### Evolf helps you break state of the art Neural Networks Loss Functions. 
#### Evolf is setup such that it can be optimized for:
    1) Time
    2) Accuracy
    3) Data
    4) Neural Network Complexity

### 2) NEAT: Coming Soon...
### 3) Distributed Training: Coming Soon...

##
## To set up Mine AI on a Debian Linux Distro: 
### 1) Clone the Repo
```console
git clone https://github.com/aj132608/mine-ai.git
```
### 2) Run the Setup
```console
cd mine-ai
bash setup.sh
```

### 3) Run an Experiment: To start your own experiment look at evolf/domains/mnist.
We provide a default domain that aims to find a record breaking loss function
for a very sparse MNIST Neural Network.

To set the experiment up:

##### 1) Open:
```console
mine-ai/evolf/domains/mnist/config.hocon
```

##### 2) Modify the following variables to your own paths:
```console
evaluator_specs > model_path
medium_model_path
small_model_path
state_of_the_art_config > model_path
output_path
```

##### 3) Run the following command and let Evolf evolve MNIST
```console
python3 -m evolf.domains.mnist.mnist --config="evolf/domains/mnist/config.hocon" 
```

