# C++ 库索引

本目录收录来自 vcpkg 官方端口集的 C/C++ 库索引，按语言大版本和端口名组织：

- 大版本目录：cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23
- 端口路径：`fmt` 位于 `cpp-v11/fmt/fmt.md`
- vcpkg 端口同时覆盖 C 与 C++ 生态；同一端口会出现在其可使用的后续语言标准目录中
- 当前共收录 2862 个 vcpkg 端口。

## 数据源

- vcpkg 官方仓库：https://github.com/microsoft/vcpkg
- vcpkg 端口集：https://github.com/microsoft/vcpkg/tree/master/ports
- vcpkg 版本历史：https://github.com/microsoft/vcpkg/tree/master/versions

## 生成方式

```bash
python tools/generate_index.py
```

按大版本统计：

- cpp-v11：2862 个端口
- cpp-v14：2862 个端口
- cpp-v17：2862 个端口
- cpp-v20：2862 个端口
- cpp-v23：2862 个端口

数据缓存见 [tools/cache/vcpkg-master.tar.gz](tools/cache/vcpkg-master.tar.gz)。
