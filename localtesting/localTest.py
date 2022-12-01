import serial
from timeit import default_timer as timer
import statistics
import pandas as pd

LEARN_RULES = {0: "HEBBIAN", 1: "ANTI_HEBBIAN", 2: "RANDOM_WALK"}

K_N_COMBINATIONS = ()

def populate_combinations_with_file(fileName):
    global K_N_COMBINATIONS
    file = open(fileName)
    combinations = []
    for line in file:
        parts = line.split(",")
        try:
            parsed_parts = (int(parts[0]),int(parts[1]))
            combinations.append(parsed_parts)
        except:
            print("Error in file, aborting.")
            return

    K_N_COMBINATIONS = tuple(combinations)

def populate_combinations_automatically(start_k_number, end_k_number, start_n_number, end_n_number):
    global K_N_COMBINATIONS
    combinations = []
    for k in range(start_k_number,end_k_number+1):
        for n in range(start_n_number,end_n_number+1):
            combinations.append((k,n))

    K_N_COMBINATIONS = tuple(combinations)

def ConnectToDevice(connectionPort):
    serialPort = serial.Serial(port = connectionPort, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    while(1):

        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            message = serialString.decode('Ascii').strip()
            if(message == "100"):
                print("[100]: Device initialized.")
                return
            else:
                print(message)


def start_test(k,n,l,learnRule,maxIterations, connectionPort):
    serialPort = serial.Serial(port = connectionPort, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    outputMsg = f"espTest.StartTpmTest({k},{n},{l},{learnRule},{maxIterations})\r\n"
    serialPort.write(str.encode(outputMsg))

    start = 0
    end = 0
    stimulusTimings = []
    learnTimings = []
    status = 0
    while(1):
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            message = serialString.decode('Ascii').strip()
            if(message == "201"):
                print("[201]: Stimulating...")
                start = timer()
            elif(message == "211"):
                print("[211]: Stimulating finished.")
                end = timer()
                elapsedTime = end - start
                stimulusTimings.append(elapsedTime)
            elif(message == "202"):
                print("[202]: Learning...")
                start = timer()
            elif(message == "212"):
                print("[212]: Learning finished.")
                end = timer()
                elapsedTime = end - start
                learnTimings.append(elapsedTime)
            elif(message == "300"):
                print("[300]: Done.")
                status = 1
                break
            elif(message == "401"):
                print("[400]: Memory Error")
                status = -1
                break
            else:
                print(message)

    return {'K': k, 'N': n, 'L': l, 'rule':LEARN_RULES[learnRule], 'max_steps': maxIterations, 'status': status, 'avg_stimulus': statistics.mean(stimulusTimings), 'avg_learning': statistics.mean(learnTimings)}

def automated_test(connectionPort,learnRule,maxIterations):
    results_array = []
    for k,n in K_N_COMBINATIONS:
        print(f"Starting test for: {(k,n)}")
        output = start_test(k,n,127,learnRule,maxIterations,connectionPort)
        results_array.append(output)
        print("-----------------------------")
    df = pd.DataFrame(data=results_array)
    return df

def benchmark_port(connectionPort,maxIterations):
    writer = pd.ExcelWriter("test_results.xlsx", engine='xlsxwriter')
    for i in range(3):
        df = automated_test(connectionPort=connectionPort,learnRule=i,maxIterations=maxIterations)
        df.to_excel(writer,sheet_name = LEARN_RULES[i], index=False)

    writer.save() 


# populate_combinations_with_file("combinations.csv")
populate_combinations_automatically(start_k_number=1,start_n_number=1,end_k_number=32,end_n_number=32)
ConnectToDevice("COM3")
benchmark_port("COM3",100)