## 0.22.1

- Support new QProgram serialization.

## 0.21.0

### Improvements

- Support new qililab yaml serialization of qprograms
  [#159](https://github.com/qilimanjaro-tech/qiboconnection/pull/159)

## 0.20.0

### Improvements

- Add time.sleep to tests
  [#160](https://github.com/qilimanjaro-tech/qiboconnection/pull/160)

## 0.19.0

### Deprecation

- Remove block_device() and release_device()
  [#157](https://github.com/qilimanjaro-tech/qiboconnection/pull/157)

## 0.18.0

### Feature

- Add support for compressed job descriptions and results
  [#155](https://github.com/qilimanjaro-tech/qiboconnection/pull/155)

## 0.17.0

### Feature

- Redefine execution interface
  [#148](https://github.com/qilimanjaro-tech/qiboconnection/pull/148)
- Redefine information of a device
  [#354](https://github.com/qilimanjaro-tech/qili-global-quantum-service/pull/354)
- Variational algorithms against simulators
  [#369](https://github.com/qilimanjaro-tech/qili-global-quantum-service/pull/369)

## 0.16.0

### Features

- job name and summary
  [#145](https://github.com/qilimanjaro-tech/qiboconnection/pull/145)

- Job cancellation
  [#142](https://github.com/qilimanjaro-tech/qiboconnection/pull/142)

- Add environment variables QUANTUM_SERVICE_URL and AUDIENCE_URL for a multi-client public API
  [#136](https://github.com/qilimanjaro-tech/qiboconnection/pull/136/files)

## 0.15.3

### Features

- Introduction of QProgram [#139](https://github.com/qilimanjaro-tech/qiboconnection/pull/139)

## 0.16.0

### Features

- Job cancellation
  [#142](https://github.com/qilimanjaro-tech/qiboconnection/pull/142)

## 0.15.1

### Improvements

- Adapt end2end tests to Slurm integration and show queue position
  [#135](https://github.com/qilimanjaro-tech/qiboconnection/pull/135)

### Bug fixes

- Recover test report
  [#133](https://github.com/qilimanjaro-tech/qiboconnection/pull/133)

## 0.14.6

### Bug fixes

- Restore test suite
  [#131](https://github.com/qilimanjaro-tech/qiboconnection/pull/131)

## 0.14.4

### New features since last release

- Show more information at errors coming from login calls
  [#110](https://github.com/qilimanjaro-tech/qiboconnection/pull/110)

## 0.14.3

### Bug fixes

- Fix issue with circuit parsing when no circuit was provided
  [#108](https://github.com/qilimanjaro-tech/qiboconnection/pull/108)

## 0.14.2

### Bug fixes

- Job result retrieving errors

## 0.14.0

### New features since last release

- Allow execution of multiple circuits in a single job
  [#95](https://github.com/qilimanjaro-tech/qiboconnection/pull/95)

## 0.13.3

### Improvements

- Removed session caching at login. [#101](https://github.com/qilimanjaro-tech/qiboconnection/pull/101)

## 0.13.2

### New features since last release

- Qiboconnection adds in the header the field **X-Client-Version** that can be checked by the API.
  [#100](https://github.com/qilimanjaro-tech/qiboconnection/pull/100)

## 0.13.1

### Improvements

- Removed redundant typings. [#103](https://github.com/qilimanjaro-tech/qiboconnection/pull/103/files)

## 0.13.0

### New features since last release

- Added API `login` constructor for user convenience.
  [#88](https://github.com/qilimanjaro-tech/qiboconnection/pull/88)
- Qiboconnection is type-permissive at read. This decouples backend and qiboconnection versions compatibility.
  [#86](https://github.com/qilimanjaro-tech/qiboconnection/pull/86)

### Improvements

- Removed `qiboconnection`'s own logging configuration
  [#91](https://github.com/qilimanjaro-tech/qiboconnection/pull/91)

### Documentation

- Skeleton of Sphinx documentation
  [#85](https://github.com/qilimanjaro-tech/qiboconnection/pull/85)

- Improvements on the documentation main page.
  [#89](https://github.com/qilimanjaro-tech/qiboconnection/pull/89)

### Bug fixes

- `update_runcard` now uses `PUT` method [#92](https://github.com/qilimanjaro-tech/qiboconnection/pull/92)

### Feat (2023-07-03)

- Delete a job by its ID using the endpoint of the public api.(#80)

### Feat (2023-06-29)

- Return an exception if the user want to retrieve a job that doesn't exist or execute without any device selected.(#73)

## v0.11.0 (2023-06-29)

- Release 0.11.0 [#77](https://github.com/qilimanjaro-tech/qiboconnection/pull/77)

### Feat (2023-06-13)

- Added get_job() and list_jobs() which retrieves all job data (including results) for one job and job metadata for all jobs the user has access to(#71)

## v0.9.0 (2023-05-04)

### Feat

- **api**: maintenance mode (#57)

## v0.8.0 (2023-04-25)

### Feat

- Update qibo to 0.1.12

### Fix

- upgrade test

## v0.7.2 (2023-03-15)

### Fix

- Fix qibo version to `0.1.10` to allow installation on Mac (#50)

## v0.7.1 (2023-02-06)

### Fix

- updates to Qibo v0.1.11 (#38)

## v0.7.0 (2023-02-06)

### Feat

- qibo 179 save experiment and results (#30)
- **api**: added `save_experiment`, `list_saved_experiments`, and `get_experiments` functionalities

### Fix

- updates to Qibo v0.1.10 and some dev packages (#36)

## v0.6.1 (2022-10-20)

### Fix

- **api**: missing return points in function that logs (#29)

## v0.6.0 (2022-09-22)

### Feat

- **api**: added `execute_and_return_results` function (#26)

## 0.5.0 (2022-09-15)

### Feat

- **api**: `_selected_devices` reset when using `select_device_id()` (#28)

## 0.4.3 (2022-07-21)

### Fix

- **release_device**: devices updated before release (#24)

## 0.4.2 (2022-07-14)

## 0.4.1 (2022-07-14)

### Fix

- **setup**: requirements
- **setup**: pythonpublish.yml action
- :bug: re-raise the errors catched
- **setup**: requirements

## 0.4.0 (2022-07-13)

### Feat

- **TII**: all changes from TII visit
- **plotting**: True 2D Plotting
- **plotting**: True 2D Plotting
- use .qibo_configuration folder (#16)
- **Plotting**: First-version

### Fix

- **plotting**: ListDevices
- **plotting**: LivePlotting

### Refactor

- using list of generic device instead of specific subclasses devices

## 0.3.9 (2022-04-08)

## v0.3.9 (2022-03-10)

## v0.0.2 (2022-02-07)

### Feat

- sending slack messages when device is in use (#4) (#5)
- using device status on remote DDBB
- sending slack messages when device is in use
