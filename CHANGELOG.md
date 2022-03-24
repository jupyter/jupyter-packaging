# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

## 0.12.0

([Full Changelog](https://github.com/jupyter/jupyter-packaging/compare/0.11.1...cdda1ad104dc5f2b27346f75c622a0ab851734c8))

### Bugs fixed

- Update import for new setuptools path (setuptools >=61.0.0) [#131](https://github.com/jupyter/jupyter-packaging/pull/131) ([@timkpaine](https://github.com/timkpaine))
- Use pathlib rather than os.path [#125](https://github.com/jupyter/jupyter-packaging/pull/125) ([@fcollonval](https://github.com/fcollonval))

### Maintenance and upkeep improvements

- Add source URL to pypi project page [#129](https://github.com/jupyter/jupyter-packaging/pull/129) ([@manics](https://github.com/manics))
- Add pre-commit [#126](https://github.com/jupyter/jupyter-packaging/pull/126) ([@fcollonval](https://github.com/fcollonval))
- Stop using distutils.log [#123](https://github.com/jupyter/jupyter-packaging/pull/123) ([@blink1073](https://github.com/blink1073))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyter/jupyter-packaging/graphs/contributors?from=2021-11-15&to=2022-03-24&type=c))

[@blink1073](https://github.com/search?q=repo%3Ajupyter%2Fjupyter-packaging+involves%3Ablink1073+updated%3A2021-11-15..2022-03-24&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyter%2Fjupyter-packaging+involves%3Afcollonval+updated%3A2021-11-15..2022-03-24&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyter%2Fjupyter-packaging+involves%3Amanics+updated%3A2021-11-15..2022-03-24&type=Issues) | [@timkpaine](https://github.com/search?q=repo%3Ajupyter%2Fjupyter-packaging+involves%3Atimkpaine+updated%3A2021-11-15..2022-03-24&type=Issues)

<!-- <END NEW CHANGELOG ENTRY> -->

## 0.11.1

- Fix running testsuite within virtualenv [#111](https://github.com/jupyter/jupyter-packaging/pull/111) ([@jnahmias](https://github.com/jnahmias))

## 0.11.0

- Drop support for Python 3.6 and add support for Python 3.10. [#109](https://github.com/jupyter/jupyter-packaging/pull/109) ([@blink1073](https://github.com/blink1073))

## 0.10.6

- The import of `bdist_wheel` is optional, must check for `None` before using it [#106](https://github.com/jupyter/jupyter-packaging/pull/106) ([@ellert](https://github.com/ellert))

## 0.10.5

- Fix last one hardcoded unversioned python command [#98](https://github.com/jupyter/jupyter-packaging/pull/98) ([@frenzymadness](https://github.com/frenzymadness))
- Add note about using the build package [#104](https://github.com/jupyter/jupyter-packaging/pull/104) ([@blink1073](https://github.com/blink1073))

## 0.10.4

- Handle missing yarn [#99](https://github.com/jupyter/jupyter-packaging/pull/99) ([@blink1073](https://github.com/blink1073))

## 0.10.3

- Some fixes for issues discovered during packaging [#96](https://github.com/jupyter/jupyter-packaging/pull/96) ([@frenzymadness](https://github.com/frenzymadness))
- Disallow deprecated function return incorrect results for Python 3.10 [#97](https://github.com/jupyter/jupyter-packaging/pull/97) ([@frenzymadness](https://github.com/frenzymadness))
- Fix handling of module metadata in tests [#92](https://github.com/jupyter/jupyter-packaging/pull/92) ([@blink1073](https://github.com/blink1073))

## 0.10.2

- Fix Handling of npm Parameter [#90](https://github.com/jupyter/jupyter-packaging/pull/90) ([@jtpio](https://github.com/jtpio))

## 0.10.1

- Fix Handling of Skip If Exists [#86](https://github.com/jupyter/jupyter-packaging/pull/86) ([@jtpio](https://github.com/jtpio))

## 0.10.0

- Add more options to Build [#84](https://github.com/jupyter/jupyter-packaging/pull/84) ([@jtpio](https://github.com/jtpio))

## 0.9.2

* Clean up handling of version info [#82](https://github.com/jupyter/jupyter-packaging/pull/82) ([@jtpio](https://github.com/jtpio))

## 0.9.1

* Do not run ensure_targets in develop mode [#79](https://github.com/jupyter/jupyter-packaging/pull/79) ([@jtpio](https://github.com/jtpio))

## 0.9.0

* Add ability to ensure targets [#77](https://github.com/jupyter/jupyter-packaging/pull/77) ([@jtpio](https://github.com/jtpio))
* Add version info helper function [#76](https://github.com/jupyter/jupyter-packaging/pull/76) ([@afshin](https://github.com/afshin))

## 0.8.3

* Fixes handling of backend [#75](https://github.com/jupyter/jupyter-packaging/pull/75) ([@jtpio](https://github.com/jtpio))

## 0.8.2

* Fix invalid command build [#72](https://github.com/jupyter/jupyter-packaging/pull/72) ([@xmnlab](https://github.com/xmnlab))

## 0.8.1

* Fix Usage of install_npm [#71](https://github.com/jupyter/jupyter-packaging/pull/71) ([@afshin](https://github.com/afshin))

## 0.8.0

* Proposal: Improved integration with setuptools [#69](https://github.com/jupyter/jupyter-packaging/pull/69) ([@afshin](https://github.com/afshin))
* Update changelog [#68](https://github.com/jupyter/jupyter-packaging/pull/68) ([@blink1073](https://github.com/blink1073))

## 0.7.12

* Use sdist from setuptools not distutils [#66](https://github.com/jupyter/jupyter-packaging/pull/66) ([@astrofrog](https://github.com/astrofrog))

## 0.7.11

* Fix packagedata docstring examples [#62](https://github.com/jupyter/jupyter-packaging/pull/62) ([@vidartf](https://github.com/vidartf))

## 0.7.10

* Only run build command if one is given [#61](https://github.com/jupyter/jupyter-packaging/pull/61) ([@vidartf](https://github.com/vidartf))
* Add basic test for skip_if_exists [#60](https://github.com/jupyter/jupyter-packaging/pull/60) ([@jtpio](https://github.com/jtpio))

## 0.7.9

* Fix typo in skip_if_exists [#59](https://github.com/jupyter/jupyter-packaging/pull/59) ([@jtpio](https://github.com/jtpio))

## 0.7.8

* Fix skip_if_exists logic [#58](https://github.com/jupyter/jupyter-packaging/pull/58) ([@jtpio](https://github.com/jtpio))
* test for nested source folder [#57](https://github.com/jupyter/jupyter-packaging/pull/57) ([@vidartf](https://github.com/vidartf))

## 0.7.7

* allow trailing slashes in spec [#56](https://github.com/jupyter/jupyter-packaging/pull/56) ([@vidartf](https://github.com/vidartf))

## 0.7.6

* Add local testing instructions [#55](https://github.com/jupyter/jupyter-packaging/pull/55) ([@blink1073](https://github.com/blink1073))
* feat: add skip_if_exists command to skip when paths exists [#54](https://github.com/jupyter/jupyter-packaging/pull/54) ([@maartenbreddels](https://github.com/maartenbreddels))
* Allow --prefix to work [#52](https://github.com/jupyter/jupyter-packaging/pull/52) ([@dsblank](https://github.com/dsblank))

## 0.7.4

* Import sdist from distutils instead of setuptools [#51](https://github.com/jupyter/jupyter-packaging/pull/51) ([@jasongrout](https://github.com/jasongrout))

## 0.7.2

* Require the packaging package [#49](https://github.com/jupyter/jupyter-packaging/pull/49) ([@blink1073](https://github.com/blink1073))
* Switch to gh actions [#48](https://github.com/jupyter/jupyter-packaging/pull/48) ([@blink1073](https://github.com/blink1073))

## 0.7.1

* Allow files to be excluded [#47](https://github.com/jupyter/jupyter-packaging/pull/47) ([@blink1073](https://github.com/blink1073))

## 0.7.0

* Test using pyproject.toml and modernize [#46](https://github.com/jupyter/jupyter-packaging/pull/46) ([@blink1073](https://github.com/blink1073))

## 0.6.1

* Remove brittle check for whether to run npm/yarn install [#44](https://github.com/jupyter/jupyter-packaging/pull/44) ([@blink1073](https://github.com/blink1073))

## 0.6.0

* move data files to the correct place on develop install [#41](https://github.com/jupyter/jupyter-packaging/pull/41) ([@Zsailer](https://github.com/Zsailer))

## 0.5.0

* Add changelog and update example [#37](https://github.com/jupyter/jupyter-packaging/pull/37) ([@blink1073](https://github.com/blink1073))
* Update readme to mention pep 518 [#36](https://github.com/jupyter/jupyter-packaging/pull/36) ([@blink1073](https://github.com/blink1073))
* Add handling of data_files in develop mode and add test [#35](https://github.com/jupyter/jupyter-packaging/pull/35) ([@blink1073](https://github.com/blink1073))
* do not pass absolute path to which [#33](https://github.com/jupyter/jupyter-packaging/pull/33) ([@MeggyCal](https://github.com/MeggyCal))
* which finds python executable [#32](https://github.com/jupyter/jupyter-packaging/pull/32) ([@MeggyCal](https://github.com/MeggyCal))

## 0.4.0

* Remove HERE [#30](https://github.com/jupyter/jupyter-packaging/pull/30) ([@vidartf](https://github.com/vidartf))

## 0.3.0

* Cleanup pt 2 [#29](https://github.com/jupyter/jupyter-packaging/pull/29) ([@vidartf](https://github.com/vidartf))
* Clean up [#28](https://github.com/jupyter/jupyter-packaging/pull/28) ([@vidartf](https://github.com/vidartf))
* Additional error checking in run() [#27](https://github.com/jupyter/jupyter-packaging/pull/27) ([@jmsdnns](https://github.com/jmsdnns))
* Add appveyor test dependencies [#26](https://github.com/jupyter/jupyter-packaging/pull/26) ([@vidartf](https://github.com/vidartf))
* Data spec path issues [#25](https://github.com/jupyter/jupyter-packaging/pull/25) ([@vidartf](https://github.com/vidartf))
* Fixed a broken test in test_find_packages [#22](https://github.com/jupyter/jupyter-packaging/pull/22) ([@jmsdnns](https://github.com/jmsdnns))
* Fix handling of pip install [#21](https://github.com/jupyter/jupyter-packaging/pull/21) ([@blink1073](https://github.com/blink1073))
* restore setuptools import [#20](https://github.com/jupyter/jupyter-packaging/pull/20) ([@minrk](https://github.com/minrk))
* Updates from using this as the JupyterLab basis [#19](https://github.com/jupyter/jupyter-packaging/pull/19) ([@blink1073](https://github.com/blink1073))
* Fix handling of data files [#18](https://github.com/jupyter/jupyter-packaging/pull/18) ([@blink1073](https://github.com/blink1073))
* Append data files instead of overwrite them [#17](https://github.com/jupyter/jupyter-packaging/pull/17) ([@jasongrout](https://github.com/jasongrout))
* Ensure targets [#16](https://github.com/jupyter/jupyter-packaging/pull/16) ([@vidartf](https://github.com/vidartf))
* Add option to force npm install/build [#15](https://github.com/jupyter/jupyter-packaging/pull/15) ([@vidartf](https://github.com/vidartf))
* Add basic tests + fixes for find_packages [#14](https://github.com/jupyter/jupyter-packaging/pull/14) ([@vidartf](https://github.com/vidartf))
* Fix `is_stale` for file paths [#13](https://github.com/jupyter/jupyter-packaging/pull/13) ([@vidartf](https://github.com/vidartf))
* Update package data after wrapped commands [#12](https://github.com/jupyter/jupyter-packaging/pull/12) ([@vidartf](https://github.com/vidartf))
* Adjust is_stale to use recursive mtimes [#10](https://github.com/jupyter/jupyter-packaging/pull/10) ([@vidartf](https://github.com/vidartf))
* Add `main` module [#8](https://github.com/jupyter/jupyter-packaging/pull/8) ([@vidartf](https://github.com/vidartf))
