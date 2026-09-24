# crashpad

> 标签: Apache-2.0, c++, conan, crashpad, vcpkg

## 简介

Crashpad is a crash-reporting system.
Crashpad is a library for capturing, storing and transmitting postmortem crash reports from a client to an upstream collection server. Crashpad aims to make it possible for clients to capture process state at the time of crash with the best possible fidelity and coverage, with the minimum of fuss.

Conan Center 收录：Crashpad is a crash-reporting system.

本库来自 vcpkg 官方端口集、Conan Center 官方 recipe 集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://chromium.googlesource.com/crashpad/crashpad/+/master/README.md
- vcpkg 端口：https://vcpkg.io/en/packages/crashpad
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/crashpad
- Conan Center：https://conan.io/center/recipes/crashpad
- Conan recipe 源码：https://github.com/conan-io/conan-center-index/tree/master/recipes/crashpad

## 历史版本号

- 当前版本：cci.20220219

- Conan cci.20220219

## 获取地址

vcpkg 安装：`vcpkg install crashpad`
Conan 安装：`conan install --requires=crashpad/cci.20220219`
vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/crashpad
- vcpkg 许可证：Apache-2.0
- 平台/支持条件：android | linux | osx | (windows & !uwp)
- 版本记录：https://github.com/conan-io/conan-center-index/blob/master/recipes/crashpad/config.yml
- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/versions/c-/crashpad.json
