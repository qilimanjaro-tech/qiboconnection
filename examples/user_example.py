import os
from time import sleep

from qibo import gates
from qibo.core.circuit import Circuit

from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration


def user_example() -> None:

    # Connect using credentials
    myconf = ConnectionConfiguration(user_id=1, username="my-user-name", api_key="abcdefg-hijk-lmno-pqrs-tuvwxyzABCDE")
    qibo_api = API(configuration=myconf)

    # Connect if credentials are already saved in your environment
    qibo_api = API()

    # Check connection
    qibo_api.ping()

    # List devices (if needed)
    devices = qibo_api.list_devices()
    print(devices)
    qibo_api.select_device_id(device_id=1)

    # Design circuit
    circuit = Circuit(1)
    circuit.add(gates.X(0))
    circuit.add(gates.M(0))

    # Issue an async remote execution of the circuit
    job_id = qibo_api.execute(circuit=circuit)
    print(f"job id: {job_id}")
    sleep(1)
    result = qibo_api.get_result(job_id=job_id)
    if result is not None:
        print(result)

    # Block device, do stuff directly over the device, release device
    qibo_api.block_device_id(device_id=1)
    # --- do stuff here ---
    qibo_api.release_device(device_id=1)


if __name__ == "__main__":
    print(f'QIBO_ENVIRONMENT={os.environ["QIBO_ENVIRONMENT"]}')
    user_example()
