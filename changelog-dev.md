# Release dev (development release)

This document contains the changes of the current release.

### New features since last release

- Allow execution of multiple circuits in a single job
  [#95](https://github.com/qilimanjaro-tech/qiboconnection/pull/95)
- Added API `login` constructor for user convenience.
  [#88](https://github.com/qilimanjaro-tech/qiboconnection/pull/88)
- Qiboconnection is type-permissive at read. This decouples backend and qiboconnection versions compatibility.
  [#86](https://github.com/qilimanjaro-tech/qiboconnection/pull/86)

### Improvements

- Removed `qiboconnection`'s own logging configuration
  [#91](https://github.com/qilimanjaro-tech/qiboconnection/pull/91)

### Breaking changes

### Deprecations / Removals

### Documentation

- Skeleton of Sphinx documentation
  [#85](https://github.com/qilimanjaro-tech/qiboconnection/pull/85)

- Improvements on the documentation main page.
  [#89](https://github.com/qilimanjaro-tech/qiboconnection/pull/89)

### Bug fixes

- `update_runcard` now uses `PUT` method [#91](https://github.com/qilimanjaro-tech/qiboconnection/pull/92)
