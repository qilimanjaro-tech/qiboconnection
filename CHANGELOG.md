## v.0.12.0 (2023-07-03)

### Feat

- Delete a job by its ID using the endpoint of the public api.
  [#80](https://github.com/qilimanjaro-tech/qiboconnection/pull/80)
- Return an exception if the user want to retrieve a job that doesn't exist or execute without any device selected
  [#73](https://github.com/qilimanjaro-tech/qiboconnection/pull/73)
- Parsed description in API's get_job()
  [#79](https://github.com/qilimanjaro-tech/qiboconnection/pull/79)

## v0.11.0 (2023-06-29)

- Release 0.11.0
  \[#77\] (https://github.com/qilimanjaro-tech/qiboconnection/pull/77)

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
