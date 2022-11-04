# Tree Parity Machines in ESP32

This repository implements Tree Parity Machines (TPMs) in micropython and numpy, using uLab.

For the sake of ease of use, this repository also contains auxiliary libraries that are used to test syncrhonization across the network. These libraries are microdot and a compiled release of ulab for a generic ESP32.

## Installation

- Flash the firmware to the ESP32.

- Upload the micropython programs.
  - TreeParityMachine.py contains the TPM implementation.
  - The setup folder contains optional files used for testing.
  - The microdot folder contains a web framework used only by the setup files.
    > Warning: After uploading the `boot.py` and resetting your device, you may not be able to upload files anymore. To solve this, connect to the micropython REPL and press `CTRL+C` to exit the running program. After you are able to interact with the
    > shell again, you may exit and upload the file you wish.

## Usage

If you intend to do tests with a single TPM in a device:

- Connect the device to a computer via USB. Access the serial console of the device using PuTTY, screen, minicom, or any other of your choosing.

  - Use a `115200` baudrate.

- Import the TreeParityMachine library

```python
from TreeParityMachine import TreeParityMachine
```

- Create a TPM object with `k` hidden units, `n` number of input neurons and `l` range of discrete weights.

```python
k = 7
n = 5
l = 4
test_tpm = TreeParityMachine(k,n,l)
```

- Now you can use these functions:

```python
TreeParityMachine.setStimulus(v) #Set a new stimulus. v is type: numpy array
TreeParityMachine.getWeights()
TreeParityMachine.setWeights(w)  #Set a weights. w is type: numpy array
TreeParityMachine.setRandomWeights()
TreeParityMachine.getResult() #Calculates the output.
TreeParityMachine.learn(learnRuleIndex) #Learn using its own output.
#Possible learnRule indexes:
#0-> Hebbian learning rule
#1-> Anti-Hebbian learning rule
#2-> Random-walk learning rule
```

If you would like to sync over the network you can use the microdot server found in `setup/microserver` to issue commands to your device and get results from it via HTTP requests.
TODO: Add postman documentation.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Acknowledgments

This is an implementation based on Prof. Iván F. Jirón Araya's original TPMs implementation in python. This new iteration aims to focus on the implementations of a single Tree Parity Machine, rather than the syncrhonization of multiple TPMs.

## License

License in discussion. You are explicitly forbidden to redistribute this code without linking to this repository or resell it under any circumstance.
You may download, modify and run this code for research purposes only.
