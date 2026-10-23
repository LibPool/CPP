# slick-perfmon

> 标签: MIT, c++, slick-perfmon, vcpkg

## 简介

Header-only C++20 latency measurement for code that cannot afford to be measured. ~200 cycles per stamp: one RDTSC read and a 16-byte publish to a lock-free MPMC ring. Pairing, Welford stats, histogram percentiles and file I/O happen on a collector thread or in a separate process.

本库来自 vcpkg 官方端口集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://github.com/SlickQuant/slick-perfmon
- vcpkg 端口：https://vcpkg.io/en/packages/slick-perfmon
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/slick-perfmon

## 历史版本号

- 当前版本：0.3.0

- 0.3.0
- 0.2.0
- 0.1.0

## 获取地址

vcpkg 安装：`vcpkg install slick-perfmon`
vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/slick-perfmon
- vcpkg 许可证：MIT
- 平台/支持条件：!uwp
- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/versions/s-/slick-perfmon.json
