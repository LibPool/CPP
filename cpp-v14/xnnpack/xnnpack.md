# xnnpack

> 标签: BSD-3-Clause, c++, conan, vcpkg, xnnpack

## 简介

High-efficiency floating-point neural network inference operators for mobile, server, and Web

Conan Center 收录：XNNPACK is a highly optimized library of floating-point

本库来自 vcpkg 官方端口集、Conan Center 官方 recipe 集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://github.com/google/XNNPACK
- vcpkg 端口：https://vcpkg.io/en/packages/xnnpack
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/xnnpack
- Conan Center：https://conan.io/center/recipes/xnnpack
- Conan recipe 源码：https://github.com/conan-io/conan-center-index/tree/master/recipes/xnnpack

## 历史版本号

- 当前版本：cci.20241203#1

- Conan cci.20241203
- Conan cci.20231026

## 获取地址

vcpkg 安装：`vcpkg install xnnpack`
Conan 安装：`conan install --requires=xnnpack/cci.20241203`
vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/xnnpack
- vcpkg 许可证：BSD-3-Clause
- 平台/支持条件：!(arm & windows) & !uwp & !arm32
- 版本记录：https://github.com/conan-io/conan-center-index/blob/master/recipes/xnnpack/config.yml
- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/versions/x-/xnnpack.json
