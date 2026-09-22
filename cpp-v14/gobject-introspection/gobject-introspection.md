# gobject-introspection

> 标签: c++, gobject-introspection, vcpkg

## 简介

A middleware layer between C libraries (using GObject) and language bindings.
Building (with) gobject-introspection is based on dynamic library linkage. Static builds of the core feature set are supported only for CI purposes.
The g-ir-scanner program runs executables for the target system. This limits actual cross-build support to targets supported by the host CPU.

本端口来自 vcpkg 官方端口集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://gi.readthedocs.io/en/latest/
- vcpkg 端口：https://vcpkg.io/en/packages/gobject-introspection
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/gobject-introspection

## 历史版本号

- 当前版本：1.86.0#3

- 1.86.0#3
- 1.86.0#2
- 1.86.0#1
- 1.86.0
- 1.82.0#1
- 1.82.0
- 1.72.0#9
- 1.72.0#8
- 1.72.0#7
- 1.72.0#6
- 1.72.0#5
- 1.72.0#4
- 共 18 条版本记录，完整清单见 vcpkg versions 文件。

## 获取地址

vcpkg 安装：`vcpkg install gobject-introspection`
port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/gobject-introspection
- 平台/支持条件：!(static & staticcrt)

- 版本记录：https://github.com/microsoft/vcpkg/blob/master/versions/g-/gobject-introspection.json
