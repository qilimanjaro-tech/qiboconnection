
from qibo.core.circuit import Circuit
from qibo import gates
from qiboconnection.api import API
from qiboconnection.connection import ConnectionConfiguration
import os


def user_example() -> None:

    qibo_api = API(configuration=ConnectionConfiguration({
        "user_id": 4,
        "username": "qili-test-1",
        "api_key": "1e64261c-4e51-440b-8ae2-74eb36255a4b",
    }))

    qibo_api = API()

    devices = qibo_api.list_devices()
    print(devices)
    qibo_api.select_device_id(device_id=1)

    circuit = Circuit(1)
    circuit.add(gates.X(0))
    circuit.add(gates.M(0))

    job_id = qibo_api.execute(circuit=circuit)
    print(f'job id: {job_id}')
    result = qibo_api.get_result(job_id=job_id)
    if result is not None:
        print(result)


if __name__ == '__main__':
    print(f'QIBO_ENVIRONMENT={os.environ["QIBO_ENVIRONMENT"]}')
    user_example()
