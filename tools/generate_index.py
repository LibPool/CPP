#!/usr/bin/env python3
"""Generate the LibPool C/C++ library index from the official vcpkg registry.

Layout:
  c-v11|17|23/<port>/<port>.md        (in the C repo)
  cpp-v11|14|17|20|23/<port>/<port>.md (in the CPP repo)

Run from the repo root:
    python tools/generate_index.py
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tarfile
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent.name.upper()
if REPO == "CPP":
    RELEASES = ["cpp-v11", "cpp-v14", "cpp-v17", "cpp-v20", "cpp-v23"]
    LANG_LABEL = "C++"
else:
    RELEASES = ["c-v11", "c-v17", "c-v23"]
    LANG_LABEL = "C"
USER_AGENT = "LibPool-Indexer/1.0 (+https://github.com/LibPool)"
CACHE_DIR = Path(__file__).resolve().parent / "cache"
TARBALL_URL = "https://github.com/microsoft/vcpkg/archive/refs/heads/master.tar.gz"
TARBALL_PATH = CACHE_DIR / "vcpkg-master.tar.gz"
CONAN_CENTER_ROOT = Path("D:/Temp/conan-center-index")
CONAN_PAGE = "https://conan.io/center/recipes"


@dataclass
class Port:
    name: str
    description: str = ""
    homepage: str = ""
    license: str = ""
    version: str = ""
    port_version: str = ""
    supports: str = ""
    versions: list[str] = field(default_factory=list)


@dataclass
class ConanRecipe:
    name: str
    description: str = ""
    homepage: str = ""
    license: str = ""
    versions: list[str] = field(default_factory=list)


def ensure_tarball() -> Path:
    if TARBALL_PATH.exists() and TARBALL_PATH.stat().st_size > 1_000_000:
        return TARBALL_PATH
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading vcpkg tarball...", flush=True)
    req = urllib.request.Request(TARBALL_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp, TARBALL_PATH.open("wb") as fh:
        while True:
            chunk = resp.read(1 << 16)
            if not chunk:
                break
            fh.write(chunk)
    return TARBALL_PATH


def load_ports() -> dict[str, Port]:
    tarball = ensure_tarball()
    ports: dict[str, Port] = {}
    versions_json: dict[str, list[str]] = {}
    with tarfile.open(tarball, "r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            path = member.name.replace("\\", "/")
            m = re.match(r"^vcpkg-master/ports/([^/]+)/vcpkg\.json$", path)
            if m:
                name = m.group(1)
                try:
                    data = json.loads(tar.extractfile(member).read().decode("utf-8", errors="replace"))
                except Exception:
                    data = {}
                port = ports.get(name, Port(name=name))
                desc = data.get("description") or ""
                if isinstance(desc, list):
                    desc = "\n".join(str(x) for x in desc if x)
                port.description = str(desc).strip()
                port.homepage = (data.get("homepage") or "").strip()
                lic = data.get("license")
                if isinstance(lic, list):
                    port.license = ", ".join(str(x) for x in lic if x)
                elif lic:
                    port.license = str(lic)
                port.version = str(data.get("version") or "")
                pv = data.get("port-version")
                port.port_version = "" if pv is None else str(pv)
                port.supports = str(data.get("supports") or "")
                ports[name] = port
                continue
            m = re.match(r"^vcpkg-master/versions/[^/]+/([^/]+)\.json$", path)
            if m:
                name = m.group(1)
                try:
                    data = json.loads(tar.extractfile(member).read().decode("utf-8", errors="replace"))
                except Exception:
                    data = {}
                rows = data.get("versions") or []
                versions: list[str] = []
                for row in rows:
                    ver = str(row.get("version") or "").strip()
                    if not ver:
                        continue
                    pv = row.get("port-version")
                    if pv not in (None, 0, "0"):
                        ver = f"{ver}#{pv}"
                    if ver not in versions:
                        versions.append(ver)
                versions_json[name] = versions
                continue
            m = re.match(r"^vcpkg-master/ports/([^/]+)/", path)
            if m:
                name = m.group(1)
                if name not in ports:
                    ports[name] = Port(name=name)
    for name, port in ports.items():
        port.versions = versions_json.get(name, [])[:60]
    return ports


def versions_path_for(name: str) -> str:
    if len(name) == 1:
        return f"versions/{name}/{name}.json"
    if len(name) == 2:
        return f"versions/{name}/{name}.json"
    return f"versions/{name[0]}-/{name}.json"


def conan_versions(config: Path) -> list[str]:
    if not config.is_file():
        return []
    text = config.read_text(encoding="utf-8", errors="replace")
    versions: list[str] = []
    in_versions = False
    for line in text.splitlines():
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped == "versions:":
            in_versions = True
            continue
        if not in_versions or not stripped or stripped.startswith("#"):
            continue
        if indent != 2 or stripped.startswith(("folder:", "languages:", "other:")):
            continue
        m = re.match(r'^"?([\w.+\-]+)"?\s*:', stripped)
        if m:
            versions.append(m.group(1))
    return versions


def extract_conan_attr(text: str, attr: str) -> str:
    pattern = re.compile(
        rf"^\s*{attr}\s*=\s*(" + r'"""(.*?)"""|"(.*?)"|\'(.*?)\'' + ")", re.S | re.M
    )
    m = pattern.search(text)
    if not m:
        return ""
    return (m.group(2) or m.group(3) or m.group(4) or "").strip()


def load_conan_recipes(root: Path) -> dict[str, ConanRecipe]:
    recipes: dict[str, ConanRecipe] = {}
    base = root / "recipes"
    if not base.is_dir():
        print(f"Conan Center recipe tree not found at {root}; skipping Conan source", flush=True)
        return recipes
    for recipe_dir in sorted(base.iterdir()):
        if not recipe_dir.is_dir():
            continue
        name = recipe_dir.name
        versions = conan_versions(recipe_dir / "config.yml")
        candidates = [recipe_dir / "all" / "conanfile.py"] + sorted(
            p for p in recipe_dir.rglob("conanfile.py")
            if "test_package" not in str(p).replace("\\", "/")
            and "test_v1_package" not in str(p).replace("\\", "/")
        )
        desc = homepage = license = ""
        for source in candidates:
            if not source.is_file():
                continue
            text = source.read_text(encoding="utf-8", errors="replace")
            if not desc:
                desc = extract_conan_attr(text, "description")
            if not homepage:
                homepage = extract_conan_attr(text, "homepage")
            if not license:
                license = extract_conan_attr(text, "license")
            if desc and homepage and license:
                break
        recipes[name] = ConanRecipe(
            name=name,
            description=desc,
            homepage=homepage,
            license=license,
            versions=versions,
        )
    return recipes


def readme_md(name: str, vcpkg: Port | None, conan: ConanRecipe | None) -> str:
    if not vcpkg and not conan:
        return ""
    desc_lines = []
    if vcpkg and vcpkg.description:
        desc_lines.append(vcpkg.description)
    if conan and conan.description and conan.description != (vcpkg.description if vcpkg else ""):
        desc_lines.append(f"Conan Center 收录：{conan.description}")
    if not desc_lines:
        desc_lines.append(f"{LANG_LABEL} 库 {name}，由软件包管理器收录。")
    desc = "\n\n".join(desc_lines)
    websites = []
    if vcpkg:
        if vcpkg.homepage:
            websites.append(f"- 官网：{vcpkg.homepage}")
        websites.append(f"- vcpkg 端口：https://vcpkg.io/en/packages/{urllib.parse.quote(vcpkg.name, safe='')}")
        websites.append(f"- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/{urllib.parse.quote(vcpkg.name, safe='')}")
    if conan:
        if conan.homepage and conan.homepage != (vcpkg.homepage if vcpkg else ""):
            websites.append(f"- 官网（Conan）：{conan.homepage}")
        websites.append(f"- Conan Center：{CONAN_PAGE}/{urllib.parse.quote(conan.name, safe='')}")
        websites.append(f"- Conan recipe 源码：https://github.com/conan-io/conan-center-index/tree/master/recipes/{urllib.parse.quote(conan.name, safe='')}")
    version_lines = []
    if vcpkg and vcpkg.versions:
        version_lines += [f"- {v}" for v in vcpkg.versions[:12]]
        if len(vcpkg.versions) > 12:
            version_lines.append(f"- 共 {len(vcpkg.versions)} 条 vcpkg 版本记录，完整清单见 vcpkg versions 文件。")
    if conan and conan.versions:
        version_lines += [f"- Conan {v}" for v in conan.versions[:12]]
        if len(conan.versions) > 12:
            version_lines.append(f"- 共 {len(conan.versions)} 个 Conan 版本，完整清单见 recipe config.yml。")
    if not version_lines:
        version_lines = ["- -"]
    version_lines_str = "\n".join(version_lines)
    current = vcpkg.version if vcpkg and vcpkg.version else (conan.versions[0] if conan and conan.versions else "未知")
    if vcpkg and vcpkg.port_version:
        current_display = f"{current}#{vcpkg.port_version}"
    else:
        current_display = current
    reqs = []
    source_names = []
    if vcpkg:
        source_names.append("vcpkg 官方端口集")
    if conan:
        source_names.append("Conan Center 官方 recipe 集")
    if not source_names:
        source_names.append("软件包管理器")
    if vcpkg:
        reqs.append(f"vcpkg 安装：`vcpkg install {vcpkg.name}`")
    if conan and conan.versions:
        reqs.append(f"Conan 安装：`conan install --requires={conan.name}/{conan.versions[0]}`")
    elif conan:
        reqs.append(f"Conan 安装：`conan install --requires={conan.name}/*`")
    if vcpkg:
        reqs.append(f"vcpkg port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/{vcpkg.name}")
        if vcpkg.license:
            reqs.append(f"- vcpkg 许可证：{vcpkg.license}")
        if vcpkg.supports:
            reqs.append(f"- 平台/支持条件：{vcpkg.supports}")
    if conan:
        if conan.license and conan.license != (vcpkg.license if vcpkg else ""):
            reqs.append(f"- Conan 许可证：{conan.license}")
        reqs.append(f"- 版本记录：https://github.com/conan-io/conan-center-index/blob/master/recipes/{conan.name}/config.yml")
    if vcpkg:
        reqs.append(f"- vcpkg 版本文件：https://github.com/microsoft/vcpkg/blob/master/{versions_path_for(vcpkg.name)}")
    tags = ", ".join(sorted(set(
        [LANG_LABEL.lower(), name]
        + (["vcpkg"] if vcpkg else [])
        + (["conan"] if conan else [])
        + ([vcpkg.license] if vcpkg and vcpkg.license else [])
        + ([conan.license] if conan and conan.license else [])
    )))
    dirs = "、".join(RELEASES)
    return f"""# {name}

> 标签: {tags}

## 简介

{desc}

本库来自 {'、'.join(source_names)}，已收录于 {dirs}。

## 官网

{chr(10).join(websites)}

## 历史版本号

- 当前版本：{current_display}

{version_lines_str}

## 获取地址

{chr(10).join(reqs)}
"""


def generate(root: Path, ports: dict[str, Port], conans: dict[str, ConanRecipe]) -> dict[str, int]:
    counts = defaultdict(int)
    for name in sorted(set(ports) | set(conans)):
        text = readme_md(name, ports.get(name), conans.get(name))
        if not text:
            continue
        for release in RELEASES:
            target = root / release / name
            target.mkdir(parents=True, exist_ok=True)
            (target / f"{name}.md").write_text(text, encoding="utf-8")
            counts[release] += 1
    return dict(counts)


def write_lang_readme(root: Path, ports: dict[str, Port], conans: dict[str, ConanRecipe], counts: dict[str, int]) -> None:
    lines = [
        f"# {LANG_LABEL} 库索引",
        "",
        f"本目录收录来自 vcpkg 官方端口集与 Conan Center 官方 recipe 集的 {LANG_LABEL} 库索引，按语言大版本和库名组织：",
        "",
        f"- 大版本目录：{'、'.join(RELEASES)}",
        f"- 端口路径：`fmt` 位于 `{RELEASES[0]}/fmt/fmt.md`",
        "- vcpkg 端口与 Conan recipe 同时覆盖 C 与 C++ 生态；同一库会出现在其可使用的后续语言标准目录中",
        f"- 当前共收录 vcpkg 端口 {len(ports)} 个、Conan Center recipe {len(conans)} 个，合并去重后 {len(set(ports) | set(conans))} 个库。",
        "",
        "## 数据源",
        "",
        "- vcpkg 官方仓库：https://github.com/microsoft/vcpkg",
        "- vcpkg 端口集：https://github.com/microsoft/vcpkg/tree/master/ports",
        "- vcpkg 版本历史：https://github.com/microsoft/vcpkg/tree/master/versions",
        "- Conan Center 官方索引：https://github.com/conan-io/conan-center-index",
        "- Conan Center 页面：https://conan.io/center/recipes",
        "",
        "## 生成方式",
        "",
        "```bash",
        "python tools/generate_index.py",
        "```",
        "",
        "按大版本统计：",
        "",
    ]
    lines += [f"- {k}：{v} 个端口" for k, v in counts.items()]
    lines += ["", "数据缓存见 [tools/cache/vcpkg-master.tar.gz](tools/cache/vcpkg-master.tar.gz)。", ""]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--conan", type=Path, default=CONAN_CENTER_ROOT)
    args = ap.parse_args()
    root = Path(args.out).resolve()
    ports = load_ports()
    conans = load_conan_recipes(args.conan)
    if args.limit:
        keep = set(list(ports)[: args.limit]) | set(list(conans)[: args.limit])
        ports = {k: v for k, v in ports.items() if k in keep}
        conans = {k: v for k, v in conans.items() if k in keep}
    print(f"Loaded {len(ports)} vcpkg ports, {len(conans)} Conan recipes...", flush=True)
    counts = generate(root, ports, conans)
    print("Generated per release:", json.dumps(counts, sort_keys=True), flush=True)
    write_lang_readme(root, ports, conans, counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
