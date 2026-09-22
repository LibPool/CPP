# libcds

> 标签: BSL-1.0, c++, libcds, vcpkg

## 简介

a collection of concurrent containers that don't require external (manual) synchronization for shared access, and safe memory reclamation (SMR) algorithms like Hazard Pointer and user-space RCU that is used as an epoch-based SMR.

本端口来自 vcpkg 官方端口集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://github.com/khizmax/libcds
- vcpkg 端口：https://vcpkg.io/en/packages/libcds
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/libcds

## 历史版本号

- 当前版本：2.3.3#4

- 2.3.3#4
- 2.3.3#3
- 2.3.3#2

## 获取地址

vcpkg 安装：`vcpkg install libcds`
port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/libcds
- 许可证：BSL-1.0
- 平台/支持条件：!(arm & (osx | windows)) & !uwp

- 版本记录：https://github.com/microsoft/vcpkg/blob/master/versions/l-/libcds.json
