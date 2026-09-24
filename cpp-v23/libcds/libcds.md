# libcds

> 标签: BSL-1.0, c++, conan, libcds, vcpkg

## 简介

a collection of concurrent containers that don't require external (manual) synchronization for shared access, and safe memory reclamation (SMR) algorithms like Hazard Pointer and user-space RCU that is used as an epoch-based SMR.

Conan Center 收录：C++11 library of Concurrent Data Structures.

本库来自 vcpkg 官方端口集、Conan Center 官方 recipe 集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://github.com/khizmax/libcds
- vcpkg 端口：https://vcpkg.io/en/packages/libcds
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/libcds
- Conan Center：https://conan.io/center/recipes/libcds
- Conan recipe 源码：https://github.com/conan-io/conan-center-index/tree/master/recipes/libcds

## 历史版本号

- 当前版本：2.3.3#4

- 2.3.3#4
- 2.3.3#3
- 2.3.3#2
- Conan 2.3.3

## 获取地址

vcpkg 安装：`vcpkg install libcds`
Conan 安装：`conan install --requires=libcds/2.3.3`
vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/libcds
- vcpkg 许可证：BSL-1.0
- 平台/支持条件：!(arm & (osx | windows)) & !uwp
- 版本记录：https://github.com/conan-io/conan-center-index/blob/master/recipes/libcds/config.yml
- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/versions/l-/libcds.json
