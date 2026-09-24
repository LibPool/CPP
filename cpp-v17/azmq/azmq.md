# azmq

> 标签: azmq, c++, vcpkg

## 简介

Boost Asio style bindings for ZeroMQ
This library is built on top of ZeroMQ's standard C interface and is intended to work well with C++ applications which use the Boost libraries in general, and Asio in particular.
The main abstraction exposed by the library is azmq::socket which provides an Asio style socket interface to the underlying zeromq socket and interfaces with Asio's io_service(). The socket implementation participates in the io_service's reactor for asynchronous IO and may be freely mixed with other Asio socket types (raw TCP/UDP/Serial/etc.).

本库来自 vcpkg 官方端口集，已收录于 cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23。

## 官网

- 官网：https://github.com/zeromq/azmq
- vcpkg 端口：https://vcpkg.io/en/packages/azmq
- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/azmq

## 历史版本号

- 当前版本：未知

- 1.0.3

## 获取地址

vcpkg 安装：`vcpkg install azmq`
vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/azmq
- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/versions/a-/azmq.json
