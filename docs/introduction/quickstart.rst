Quickstart
==========

.. note::

    If you don't already have a QaaS account, please request one by sending an email to: FILL EMAIL

To start using ``qiboconnection``, you just need to install the package using PyPi:

.. code-block:: console

    $ pip install qiboconnection

If you already have your username and api key, then you can open a Python script and follow the next steps to send your
first quantum job!

First of all, you must login to our API:


>>> from qiboconnection import API
>>> api = API.login(username="qat", api_key="meow")
[qibo-connection] 0.12.0|INFO|2023-09-21 18:16:26]: Storing personal qibo configuration...

.. note::

    When logging in, a new folder named ``.qibo_configuration`` will be created in your current working directory, where
    your username, api key and access tokens will be stored.

Once you are logged in, you can list all accessible quantum processing units and simulators by using
:func:`~qiboconnection.API.list_devices`:

>>> api.list_devices()
<Devices[5]:
{
  "device_id": 9,
  "device_name": "Galadriel Qblox rack",
  "status": "online",
  "availability": "available",
  "characteristics": {
    "type": "quantum"
  },
  "calibration_details": {
    "t1": 10,
    "frequency": 988
  }
}
{
  "device_id": 1,
  "device_name": "Radagast Simulator",
  "status": "offline",
  "availability": "available"
}

You can then use :func:`~qiboconnection.API.select_device_id` or :func:`~qiboconnection.API.select_device_ids` to select
one or multiple devices where your quantum jobs will be executed:

>>> api.select_device_id(device_id=9)
[qibo-connection] 0.12.0|INFO|2023-09-21 18:21:29]: Device Galadriel Qblox rack selected.

Now you are ready to create and execute your first quantum job! To do so, we will use
`Qibo <https://qibo.science/qibo/stable/>`_, an open-source quantum API, to build the quantum circuit that we want to
execute:

.. code-block:: python3

    from qibo import Circuit, gates

    c = Circuit(2)
    c.add(gates.X(0))
    c.add(gates.CNOT(0, 1))
    c.add(gates.M(0, 1))

To execute the circuit, you just need to do:

>>> api.execute(circuit=c)
[1168]

The :func:`~qiboconnection.API.execute` method returns a list of integers, which correspond to the indexes of the jobs
executed in all the devices we selected. Given that we just selected one device, we obtained only one value.

.. note::

    You can retrieve the indexes of all the jobs executed during a session by using the :func:`~qiboconnection.API.jobs`
    property:

    >>> [job.id for job in api.jobs]
    [1168]

To see the status of a job, we can use the :func:`~qiboconnection.API.get_result` method:

>>> result = api.get_result(job_id=1168)
[qibo-connection] 0.12.0|WARNING|2023-09-21 18:38:11]: Your job with id 1168 is still pending. Job queue position: 2

.. note::

    If the job has not been executed yet, the :func:`~qiboconnection.API.get_result` method returns ``None``.

Once our job is executed, this same method will return the obtained results:

>>> result = api.get_result(job_id=1168)
>>> print(result)
???????
