# Changelog

## [3.2.0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v3.1.2...v3.2.0) (2026-06-23)


### Features

* add activate_trial method to PolarionRestApiConnection ([#81](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/81)) ([f6b70b3](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/f6b70b3b787fb2abd6201b7a99b5d01151623fc2)), closes [#80](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/80)
* support custom com.polarion.alm.* extensions (enumerationfactories, vcontext) ([#83](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/83)) ([fe70e15](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/fe70e156569f14b3f2e2bc69e8c112f7cd2d5f87)), closes [#82](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/82)


### Bug Fixes

* prevent path injection in project manager ([#78](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/78)) ([be2eb4c](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/be2eb4c1a48077ea30122b5c23636405974b994a))

## [3.1.2](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v3.1.1...v3.1.2) (2026-06-17)


### Bug Fixes

* forward host timezone to Polarion JVM in container ([#75](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/75)) ([2510b6d](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/2510b6d9702f7bbe3056eee23d50e9974e27b075)), closes [#74](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/74)

## [3.1.1](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v3.1.0...v3.1.1) (2026-06-17)


### Bug Fixes

* increase timeout and token expiration for Polarion API ([#70](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/70)) ([d38fbbd](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/d38fbbd6143bc95d9978426378b7657eb9497cf9)), closes [#69](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/69)

## [3.1.0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v3.0.0...v3.1.0) (2026-06-12)


### Features

* support nesting temp projects under a project group via parent_location ([#66](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/66)) ([8e6b3f0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/8e6b3f04e9f3574e49361604cafed3b95b0b4aae)), closes [#67](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/67)

## [3.0.0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.1.1...v3.0.0) (2026-06-10)


### ⚠ BREAKING CHANGES

* deprecate admin utility methods in favor of standard Polarion API ([#65](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/65))
* add new endpoints for LLMs and document operations in Polarion 2606 ([#61](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/61))

### Features

* add new endpoints for LLMs and document operations in Polarion 2606 ([#61](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/61)) ([673cb34](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/673cb349363c64566b21d43890a7c70e41c69e94)), closes [#60](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/60)
* deprecate admin utility methods in favor of standard Polarion API ([#65](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/65)) ([ed0c069](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/ed0c069c90ac0af6d5b05341f73162a62e325b7d)), closes [#62](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/62)
* enhance project management with asynchronous creation and deletion using standard Polarion REST API ([#64](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/64)) ([072aae1](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/072aae1f20384a5d54fe2a544ff6bb5527432977)), closes [#62](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/62)

## [2.1.1](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.1.0...v2.1.1) (2026-06-09)


### Bug Fixes

* xml-repair endpoints actualization ([#58](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/58)) ([4aaba5a](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/4aaba5a338ca8c5fd1cbc3327110706fe78f4bda))

## [2.1.0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.0.3...v2.1.0) (2026-06-01)


### Features

* Integrity-Scanner extension ([#55](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/55)) ([1759ca8](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/1759ca8723601356dc893f595868c1f83516f5d9)), closes [#54](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/54)

## [2.0.3](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.0.2...v2.0.3) (2026-04-08)


### Bug Fixes

* add pull-requests:read to actionlint caller permissions ([#44](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/44)) ([83b486f](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/83b486f9528540c1b05f5432acda2097575d097c))
* add pull-requests:read to actionlint caller permissions ([#46](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/46)) ([83b486f](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/83b486f9528540c1b05f5432acda2097575d097c))
* not all endpoints declared for xml-repair ([#51](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/51)) ([9df641a](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/9df641af2f07d06cd1e0612ea7a0d37548782213)), closes [#50](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/50)
* use github.ref_name for SonarCloud push scan branch name ([#42](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/42)) ([ffcdf47](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/ffcdf4776a5f789dff27e0961992f5d9ee5da25d)), closes [#27](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/27)

## [2.0.2](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.0.1...v2.0.2) (2026-03-30)


### Bug Fixes

* release-please CI fixes ([#38](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/38)) ([3f8cbed](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/3f8cbed5c4c473f6c7d838b7bcb010f359640a7c))

## [2.0.1](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/compare/v2.0.0...v2.0.1) (2026-03-30)


### Bug Fixes

* use --frozen instead of --locked in CI workflow ([#33](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/33)) ([5ce770a](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/5ce770a0402c45cbd89c026f5f85020974e9b47d)), closes [#32](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/32)

## 2.0.0 (2026-03-30)


### Features

* added test-data for testcontainers ([#30](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/30)) ([9c522ed](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/9c522ed3a6fdc112df679ca54b10ee3a7629db4e)), closes [#29](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/29)
* migrate from Bitbucket to GitHub ([4448bb8](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/4448bb80499353723ac305c38a47b23de2f4c24c))
* rename qa to req inspector ([9355ba4](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/9355ba4e555b9aa7f2a7e3f0ca8519aff8897575))


### Bug Fixes

* **deps:** update dependency requests to v2.32.4 ([9314f29](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/9314f29b30dd6314e450ecf85aa5d802049adb39))
* **deps:** update dependency requests to v2.32.4 [security] ([21da0d0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/21da0d081529cca8835e287adac160b8e31987be))
* **deps:** update dependency requests to v2.32.5 ([70a6b67](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/70a6b67c435c53cec6c5749891826e73a25367a4))
* **deps:** update dependency testcontainers to v4 ([#4](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/4)) ([7ccd4ed](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/7ccd4edffe3b9f9a8363a1d7c6dfe62236fc0dba))
* **deps:** update dependency testcontainers to v4.10.0 ([add6500](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/add6500163c4ba32560a7f7942cb54867847c0da))
* **deps:** update dependency testcontainers to v4.12.0 ([10ebbb2](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/10ebbb25d36606158e9d83e13eda340eefbaf3ba))
* **deps:** update dependency testcontainers to v4.13.0 ([4c2f1f1](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/4c2f1f1d55e7f769b52bf4a433ffc3d9d4ab147b))
* **deps:** update dependency testcontainers to v4.13.1 ([c39c7e0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/c39c7e0db338dc01704b5fdddb82f58028b00705))
* **deps:** update dependency testcontainers to v4.13.2 ([833b26b](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/833b26b5e66ee33790dffc079067ebde33004227))
* **deps:** update dependency testcontainers to v4.13.3 ([3bf4b45](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/3bf4b45945ba3caf80c512ee1b58c0b4e1a44e0f))
* **deps:** update dependency testcontainers to v4.14.0 ([#13](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/13)) ([1a1cd24](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/1a1cd245b2c69f4c1d84900b3fcb6b9480637738))
* **deps:** update dependency testcontainers to v4.14.1 ([79b8e67](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/79b8e675a930cb2f4ec5f82b85bda067ea781385))
* exclude polarion API from sonar duplication check ([#24](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/24)) ([ad90341](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/ad90341f2216e8c986cea9be3c6a8098078cebe5))
* extract pagination string literals into constants ([#19](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/19)) ([33a78e4](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/33a78e49f6dc19cc2fc9a0133784665953c3f9ac)), closes [#18](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/18)
* move package=skip to ruff/mypy envs only ([#16](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/16)) ([6179b46](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/6179b46904017cbab6d329d584de0e6d268180f9))
* poetry-build.yml ([0794f03](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/0794f03a74c971a802c86ee17bd2d43490fd724c))
* poetry-build.yml ([ac6dad3](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/ac6dad327380560ecc00b6ed4d9fb575c1f39be8))
* release-please config ([77bd7b7](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/77bd7b7a7b36ac3f097557dadd7773b558e2ea84))
* resolve SonarCloud issues in verification code ([#20](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/20)) ([e87fc0b](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/e87fc0b3fef2d5fcc3ef5f6a472bfeb871cc19bc)), closes [#18](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/18)
* update test assertions to match lazy logging format ([ed77f1e](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/ed77f1ea937cfe8937267f9f9b935d010ccee2a9))


### Performance Improvements

* switch tox to uv-venv-lock-runner for faster CI ([#15](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/issues/15)) ([68d4ca0](https://github.com/SchweizerischeBundesbahnen/python-sbb-polarion/commit/68d4ca0666943b35e19c050273e7a5fede212518))
