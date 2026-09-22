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


def readme_md(port: Port) -> str:
    current = port.version or (port.versions[0] if port.versions else "未知")
    if port.port_version:
        current_display = f"{current}#{port.port_version}"
    else:
        current_display = current
    version_lines = "\n".join(f"- {v}" for v in port.versions[:12])
    if not version_lines:
        version_lines = "- -"
    if len(port.versions) > 12:
        version_lines += f"\n- 共 {len(port.versions)} 条版本记录，完整清单见 vcpkg versions 文件。"
    websites = []
    if port.homepage:
        websites.append(f"- 官网：{port.homepage}")
    websites.append(f"- vcpkg 端口：https://vcpkg.io/en/packages/{urllib.parse.quote(port.name, safe='')}")
    websites.append(f"- vcpkg 源码：https://github.com/microsoft/vcpkg/tree/master/ports/{urllib.parse.quote(port.name, safe='')}")
    reqs = [f"vcpkg 安装：`vcpkg install {port.name}`", f"port 目录：https://github.com/microsoft/vcpkg/tree/master/ports/{port.name}"]
    if port.license:
        reqs.append(f"- 许可证：{port.license}")
    if port.supports:
        reqs.append(f"- 平台/支持条件：{port.supports}")
    desc = port.description or f"vcpkg 端口 {port.name}，由 vcpkg C/C++ 软件包管理器收录。"
    tags = ", ".join(sorted(set([LANG_LABEL.lower(), "vcpkg", port.name] + ([port.license] if port.license else []))))
    dirs = "、".join(RELEASES)
    return f"""# {port.name}

> 标签: {tags}

## 简介

{desc}

本端口来自 vcpkg 官方端口集，已收录于 {dirs}。

## 官网

{chr(10).join(websites)}

## 历史版本号

- 当前版本：{current_display}

{version_lines}

## 获取地址

{chr(10).join(reqs)}

- 版本记录：https://github.com/microsoft/vcpkg/blob/master/{versions_path_for(port.name)}
"""


def generate(root: Path, ports: dict[str, Port]) -> dict[str, int]:
    counts = defaultdict(int)
    for name in sorted(ports):
        port = ports[name]
        text = readme_md(port)
        for release in RELEASES:
            target = root / release / name
            target.mkdir(parents=True, exist_ok=True)
            (target / f"{name}.md").write_text(text, encoding="utf-8")
            counts[release] += 1
    return dict(counts)


def write_lang_readme(root: Path, ports: dict[str, Port], counts: dict[str, int]) -> None:
    lines = [
        f"# {LANG_LABEL} 库索引",
        "",
        "本目录收录来自 vcpkg 官方端口集的 C/C++ 库索引，按语言大版本和端口名组织：",
        "",
        f"- 大版本目录：{'、'.join(RELEASES)}",
        f"- 端口路径：`fmt` 位于 `{RELEASES[0]}/fmt/fmt.md`",
        "- vcpkg 端口同时覆盖 C 与 C++ 生态；同一端口会出现在其可使用的后续语言标准目录中",
        f"- 当前共收录 {len(ports)} 个 vcpkg 端口。",
        "",
        "## 数据源",
        "",
        "- vcpkg 官方仓库：https://github.com/microsoft/vcpkg",
        "- vcpkg 端口集：https://github.com/microsoft/vcpkg/tree/master/ports",
        "- vcpkg 版本历史：https://github.com/microsoft/vcpkg/tree/master/versions",
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
    args = ap.parse_args()
    root = Path(args.out).resolve()
    ports = load_ports()
    if args.limit:
        ports = dict(sorted(ports.items())[: args.limit])
    print(f"Loaded {len(ports)} vcpkg ports...", flush=True)
    counts = generate(root, ports)
    print("Generated per release:", json.dumps(counts, sort_keys=True), flush=True)
    write_lang_readme(root, ports, counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
