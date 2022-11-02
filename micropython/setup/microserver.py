import uasyncio
import network_manager
from TreeParityMachine import TreeParityMachine
from microdot_asyncio import Microdot
from ulab import numpy as np
import urequests
import ujson
# setup webserver
app = Microdot()
localTree = TreeParityMachine(3,3,127)

@app.post('/debug')
async def debug(request):
    print(request.json['test'])
    return request.json['test']

@app.route('/')
async def hello(request):
	return network_manager.get_local_ip()

@app.post('/init')
async def initializeTPM(request):
    k = (request.json['k'])
    n = (request.json['n'])
    l = (request.json['l'])
    uasyncio.create_task(initialize_local_machine(k,n,l))
    return "OK!"

@app.post('/debug-set-weights')
async def stimulateTPM(request):
    weights_raw = request.json['weights']
    uasyncio.create_task(parse_and_set_weights(weights_raw))
    return "Got weights!"

@app.post('/stimulate')
async def stimulateTPM(request):
    stimulus_raw = request.json['stimulus']
    uasyncio.create_task(parse_and_stimulate(stimulus_raw))
    return "Stimulating!"

@app.get('/calculate')
async def calculateTPM(request):
    uasyncio.create_task(calculate_and_send(localTree.getResult()))
    return "Calculating output..."

@app.post('/stimulate-and-calculate')
async def stimulateTPM(request):
    stimulus_raw = request.json['stimulus']
    print("!Got stimulus:")
    uasyncio.create_task(stimulate_and_calculate(stimulus_raw))
    return "Stimulating and calculating!"

@app.post('/train')
async def trainTPM(request):
    learnRule = request.json['learningRule']
    uasyncio.create_task(learn_and_send_weights(learnRule))
    return "Learning..."

def start_server():
    print('Starting microdot app')
    try:
        uasyncio.create_task(register_in_server())
        app.run(port=80)
    except:
        app.shutdown()

#Async functions
async def initialize_local_machine(k,n,l):
    global localTree
    localTree = TreeParityMachine(k,n,l)
    print("Initialized local tree: ", localTree.getWeights())
    uasyncio.run(send_weights(localTree.getWeights()))
    return

async def parse_and_set_weights(raw_weights):
    # print(raw_stimulus)
    weights_parsed = np.array(raw_weights)
    # print("Recieved stimulus: ", stimulus_parsed)
    localTree.setWeights(weights_parsed)
    return

async def parse_and_stimulate(raw_stimulus):
    print(raw_stimulus)
    stimulus_parsed = np.array(raw_stimulus)
    # print("Recieved stimulus: ", stimulus_parsed)
    localTree.setStimulus(stimulus_parsed)
    return

async def calculate_and_send(output):
    post_data = ujson.dumps({"ip":network_manager.get_local_ip(),"output":output})
    print("!!!Calculating")
    # print(post_data)
    url = network_manager.get_server_dir("OUTPUT")
    try:
        req = urequests.post(url, headers = {'content-type': 'application/json'}, data = post_data)
        print(req.status_code)
    except Exception as e:
        print("ERROR: when sending output!")
        print(str(e))
    return

async def stimulate_and_calculate(raw_stimulus):
    stimulation_task = uasyncio.create_task(parse_and_stimulate(raw_stimulus))
    await stimulation_task
    output = localTree.getResult()
    uasyncio.run(calculate_and_send(output))
    return

async def learn_and_send_weights(learnRule):
    localTree.learn(learnRule)
    print("!!!Learning!")
    uasyncio.run(send_weights(localTree.getWeights()))
    return

async def send_weights(tpm_weights):
    weights = tpm_weights.tolist() #HAY QUE PARSEAR LOS WEIGHTS O TIRA BAD REQUEST
    # print(weights)
    post_data = ujson.dumps({"ip":network_manager.get_local_ip(),"weights":weights})
    url = network_manager.get_server_dir("WEIGHTS")
    try:
        req = urequests.post(url, headers = {'content-type': 'application/json'}, data = post_data)
        print(req.status_code)
    except Exception as e:
        print("ERROR: When sending weights!")
        print(str(e))
    return

async def register_in_server():
    post_data = ujson.dumps({"ip":network_manager.get_local_ip()})
    url = network_manager.get_server_dir("INIT")
    # print(url)
    try:
        urequests.post(url, headers = {'content-type': 'application/json'}, data = post_data)
    except Exception as e:
        print("ERROR: on register!")
        print(str(e))
        network_manager.connect_to_wifi()
    return

async def connect_to_wifi():
    task = uasyncio.create_task(network_manager.connect_to_wifi())
    await task

local_ip = ""
# connect_to_wifi()
network_manager.connect_to_wifi()
local_ip = (network_manager.get_local_ip())
print(local_ip)
start_server()
