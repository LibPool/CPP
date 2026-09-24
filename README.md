# C++ 库索引

本目录收录来自 vcpkg 官方端口集与 Conan Center 官方 recipe 集的 C++ 库索引，按语言大版本和库名组织：

- 大版本目录：cpp-v11、cpp-v14、cpp-v17、cpp-v20、cpp-v23
- 端口路径：`fmt` 位于 `cpp-v11/fmt/fmt.md`
- vcpkg 端口与 Conan recipe 同时覆盖 C 与 C++ 生态；同一库会出现在其可使用的后续语言标准目录中
- 当前共收录 vcpkg 端口 2862 个、Conan Center recipe 1950 个，合并去重后 3791 个库。

## 数据源

- vcpkg 官方仓库：https://github.com/microsoft/vcpkg
- vcpkg 端口集：https://github.com/microsoft/vcpkg/tree/master/ports
- vcpkg 版本历史：https://github.com/microsoft/vcpkg/tree/master/versions
- Conan Center 官方索引：https://github.com/conan-io/conan-center-index
- Conan Center 页面：https://conan.io/center/recipes

## 生成方式

```bash
python tools/generate_index.py
```

按大版本统计：

- cpp-v11：3791 个端口
- cpp-v14：3791 个端口
- cpp-v17：3791 个端口
- cpp-v20：3791 个端口
- cpp-v23：3791 个端口

数据缓存见 [tools/cache/vcpkg-master.tar.gz](tools/cache/vcpkg-master.tar.gz)。
