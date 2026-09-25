# AstrBot 表情包规范

[English](ASTRBOT_MEME_PACK_PROTOCOL.md)

- 文档修订版本：0.3
- 清单模式版本：`1`
- 可选语义扩展版本：`1`
- 语义元数据模式版本：`"2.0"`

## 1. 适用范围

本规范定义 AstrBot 表情包的可交换内容，包括目录结构、清单、分类图片资源、预览图及可选的语义描述。官方、社区及私有分发的表情包均适用同一格式。

本规范不规定应用的存储位置、已安装包注册表、人格或会话选择、提示词、检索算法、模型调用、WebUI 布局、下载或安装流程、备份管理及迁移行为。社区索引与收录要求属于仓库政策，见 [README](README.md#社区索引格式与收录要求)，不属于包格式符合性的判定条件。

修订版本 0.3 取代版本 0.2 中面向具体实现的范围定义，不改变现有 JSON Schema 及其版本号。表情包的身份由清单确定，与其所在目录的名称无关。

## 2. 术语与要求等级

- **包根目录**：包含 `manifest.json` 和 `memes/` 的目录。
- **清单**：以 UTF-8 编码的 JSON 对象，存储于 `manifest.json`，用于描述表情包。
- **分类**：具有名称且在清单中附有描述的一组图片。
- **基础包**：由清单和分类图片资源组成、不要求任何扩展的表情包。
- **语义扩展**：与具体图片文件关联的可选逐图描述。

**必须（MUST）**和**不得（MUST NOT）**表示强制要求。**应当（SHOULD）**和**不应（SHOULD NOT）**表示建议，在有合理理由时可以偏离。**可以（MAY）**表示可选项。示例用于说明；字段约束和符合性要求具有规范性。

[清单 Schema](schemas/meme-pack-manifest.schema.json) 和[语义元数据 Schema](schemas/meme-pack-semantic.schema.json) 定义 JSON 类型、允许的属性、长度与模式约束，对应文档必须通过相应 Schema 校验。下文规定的文件关联与内容校验要求是 JSON Schema 校验之外的补充要求。

## 3. 包结构

```text
<pack_root>/
  manifest.json
  memes/
    happy/
      smile.png
    sad/
      tears.gif
  previews/
    cover.png
  semantic_metadata.json
```

包根目录中必须存在 `manifest.json` 和 `memes/`。`previews/` 与 `semantic_metadata.json` 为可选内容。包根目录可以使用任意名称，也可以是仓库根目录或子目录，无须与清单中的 `id` 一致。

表情图片必须按 `memes/<category>/<image>` 存放，分类目录名必须与清单中的相应分类键完全一致。本规范不规定固定的分类词表。

包中可以附带 README、许可文件、来源说明等文档。这些文档不属于表情图片资源，也不能替代清单字段。

## 4. 清单

### 4.1 必填字段

| 字段 | 类型 | 要求 |
| --- | --- | --- |
| `schema_version` | 整数 | 必须为 `1` |
| `id` | 字符串 | 稳定的包标识符，长度为 2–64 个字符，匹配 `^[a-z0-9][a-z0-9._-]{1,63}$` |
| `name` | 字符串 | 显示名称，长度为 1–128 个字符 |
| `version` | 字符串 | 包的发布版本标识，长度为 1–64 个字符；建议使用语义化版本 |
| `categories` | 对象 | 至少包含一个分类；每个分类值必须包含 `description` |

同一表情包在不同版本之间应当保持 ID 不变，且应当使用能够区别于其他已发布表情包的 ID。`version` 标识包内容的发布版本，独立于文档版本、模式版本及扩展版本。

分类键必须匹配 `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`。每个分类值必须是包含 `description` 字符串的对象，描述长度为 1–2000 个字符。描述应当说明分类的含义或适用场景，不规定应用如何构建提示词或选择图片。

### 4.2 可选字段

可选字段可以省略；提供时必须满足下列约束及清单 Schema。

| 字段 | 类型 | 含义与约束 |
| --- | --- | --- |
| `description` | 字符串 | 包简介，长度为 1–2000 个字符；建议提供 |
| `author` | 字符串 | 作者或署名，长度为 1–128 个字符 |
| `homepage` | 字符串 | 主页 URI，最多 2048 个字符 |
| `license` | 字符串 | 许可标识或许可信息引用，长度为 1–256 个字符；建议提供 |
| `tags` | 字符串数组 | 最多 32 个不重复的标签，每项长度为 1–64 个字符 |
| `icon` | 字符串 | 相对于包根目录的图片路径，长度为 1–512 个字符 |
| `previews` | 字符串数组 | 最多 32 个不重复的包内相对图片路径，每项长度为 1–512 个字符 |
| `source` | 对象 | 第 4.3 节定义的来源描述符 |
| `compat` | 对象 | 可以包含 `min_plugin_version`，以长度为 1–64 个字符的字符串说明兼容的最低表情包管理插件版本 |
| `extensions` | 对象 | 可选扩展声明；语义扩展声明见第 6 节 |

应当提供图标和预览图以便展示，但缺少这些内容不会导致基础包无效。清单不允许额外的顶层属性；扩展声明应放在 `extensions` 中，该对象允许额外的扩展名称。本规范不为未知扩展名称定义可交换的行为。

### 4.3 来源描述符

提供 `source` 时，下列四个字段必须全部存在。来源描述符用于标识包的来源，不要求采用特定的下载或安装流程。

| 字段 | 要求 |
| --- | --- |
| `type` | 字符串 `"github"` |
| `repo` | `owner/repo` 形式的仓库标识，匹配 `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`，最多 200 个字符 |
| `ref` | 非空的分支、标签或提交引用，最多 200 个字符 |
| `subpath` | 相对于仓库根目录的包根目录路径，长度为 1–512 个字符；仓库根目录使用 `"."` |

`subpath` 必须满足 Schema 的相对目录路径约束，不得为绝对路径、包含反斜杠或 `..`，也不得解析到仓库之外。

### 4.4 最小清单示例

```json
{
  "schema_version": 1,
  "id": "example-pack",
  "name": "Example Meme Pack",
  "version": "1.0.0",
  "categories": {
    "happy": {
      "description": "Express joy, positive feedback, or celebration."
    }
  }
}
```

该示例仅需配套 `manifest.json` 及 `memes/happy/` 下的分类图片资源，无须提供预览字段或语义元数据。

### 4.5 扩展清单示例

```json
{
  "schema_version": 1,
  "id": "example-pack",
  "name": "Example Meme Pack",
  "version": "1.0.0",
  "description": "Images for everyday conversations.",
  "author": "Example Author",
  "homepage": "https://github.com/example/meme-pack",
  "license": "SEE LICENSE IN LICENSE",
  "tags": ["daily", "reaction"],
  "icon": "previews/cover.png",
  "previews": ["previews/cover.png"],
  "source": {
    "type": "github",
    "repo": "example/meme-pack",
    "ref": "main",
    "subpath": "."
  },
  "categories": {
    "happy": {
      "description": "Express joy, positive feedback, or celebration."
    }
  },
  "extensions": {
    "semantic": {
      "version": 1,
      "file": "semantic_metadata.json"
    }
  }
}
```

所引用的预览图及所声明的语义元数据文件必须存在。语义元数据必须针对该包 ID 及图片文件满足第 6 节的要求。

## 5. 图片资源与路径

基础图片格式为 PNG（`.png`）、JPEG（`.jpg`、`.jpeg`）、GIF（`.gif`）和 WebP（`.webp`），适用于表情图片和预览图。其他图片格式不在本规范的互操作保证范围内。

包内资源的相对路径必须使用 `/` 作为分隔符，并指向包根目录内实际存在的文件。不得使用绝对路径、外部 URL 或逃逸包根目录的路径，包括通过符号链接逃逸。清单的 `icon` 与 `previews` 路径还必须满足 Schema 约束，其中禁止反斜杠及任何 `..` 子串。语义图片路径另须满足第 6 节规定的具体结构。

预览图应当放在 `previews/` 中。预览图用于展示包内容；只有同时作为 `memes/` 下的资源并在 `categories` 中声明相应分类时，才属于分类图片资源。

可执行文件和脚本不属于图片资源，不得作为表情图片处理。包内的描述及其他元数据属于数据，不构成执行命令的授权。

## 6. 可选语义描述

<a id="75-可选语义描述扩展"></a>

### 6.1 可选性与声明

基础包不包含语义元数据时仍然完整有效。语义文件可以描述任意部分的图片，也可以不包含任何图片记录。逐图描述是必填分类描述的补充。

可选的 `extensions.semantic` 声明必须包含 `version: 1` 和 `file: "semantic_metadata.json"`，且不得包含额外属性。声明后，该文件必须位于包根目录。为兼容已有导出包，也可以仅提供使用这一固定名称的有效文件而不添加声明。

文件必须为 UTF-8 编码的 JSON 对象，符合[语义元数据 Schema](schemas/meme-pack-semantic.schema.json)。扩展版本 `1`、元数据模式版本 `"2.0"` 和清单模式版本 `1` 是相互独立的标识。

### 6.2 元数据字段

| 字段 | 要求 |
| --- | --- |
| `schema_version` | 字符串 `"2.0"` |
| `pack_id` | 必须等于清单中的 `id` |
| `images` | 以 `entry_id` 为键的对象；允许为空或仅覆盖部分图片 |
| `images.*.entry_id` | 64 位小写十六进制字符；必须与记录键一致 |
| `images.*.content_sha256` | 图片原始文件字节的 SHA-256 摘要，以 64 位小写十六进制字符表示 |
| `images.*.relative_path` | 实际存在的图片路径，格式为 `memes/<category>/<filename>`，使用 `/` 分隔，不含额外目录层级 |
| `images.*.category` | 清单中已有的分类键，必须与路径中的分类部分完全一致 |
| `images.*.caption` | 描述字符串；`caption_status` 不为 `done` 时可以为空 |
| `images.*.caption_status` | `pending`、`running`、`done` 或 `failed`；`done` 要求描述至少包含一个非空白字符 |
| `images.*.tags` | 可选的不重复字符串数组 |
| `images.*.visible_text` | 可选字符串，记录图片中可见的文字 |
| `images.*.provenance` | 可选字符串，说明描述的来源 |

上表除 `tags`、`visible_text` 和 `provenance` 外均为必填字段。`caption_status` 沿用现有格式中的取值，不规定处理工作流。

### 6.3 图片身份

`entry_id` 必须是以下内容经 UTF-8 编码后计算得到的 SHA-256 摘要，以小写十六进制表示：

```text
content_sha256 + NUL + category + NUL + relative_path
```

`NUL` 表示一个零字节。计算时使用实际存储的分类与相对路径，因此内容相同但路径或分类不同的图片具有不同的条目 ID。

内容哈希必须与所引用的文件一致。记录键、`entry_id` 和计算得到的条目 ID 必须一致。解析后的图片路径必须仍位于包内 `memes/` 目录中，包括解析符号链接后的路径。图片字节、分类或相对路径发生变化时，必须更新相应的身份字段及记录键。

包含实际图片、匹配哈希及校验说明的完整示例见 [examples/semantic](examples/semantic/README.md)。

### 6.4 可交换内容

描述可以由人工撰写或模型生成；本格式不要求模型服务或向量索引。公开分发的元数据不得包含凭据、私人对话或私人信息。

语义 Schema 为兼容已有文件而允许额外属性，但这些属性不具有本规范定义的可交换语义。本机服务提供商标识、处理进度及向量状态不属于包的必需内容。应用可以在不支持语义描述的情况下使用基础包。

## 7. 分发边界

表情包可以以目录、仓库子目录或归档中的文件形式分发。其可交换内容由前文定义的包根目录及其内容组成。仓库或归档的外层目录名称不作为包标识符。

使用归档承载表情包时，归档条目不得解析到解压根目录之外。本规范不定义归档容器版本、不要求特定压缩格式，也不规定应用的备份与恢复行为。

发布、社区收录、许可审核及安装与本数据格式的符合性分别处理。社区要求由 [README](README.md#社区索引格式与收录要求) 维护。

## 8. 符合性

基础包校验包含以下检查：

1. 包根目录包含可读取的 UTF-8 JSON 文件 `manifest.json` 及 `memes/` 目录。
2. 清单符合清单 Schema，包括必填字段及分类描述。
3. 表情图片遵循 `memes/<category>/<image>` 结构，分类名与清单一致。
4. 所引用的图标和预览图存在，图片资源及路径符合第 5 节要求。

语义扩展校验还须按第 6 节检查声明与文件、模式版本、包 ID、分类归属、记录键、文件存在性、内容哈希及条目 ID。仅通过 JSON Schema 校验不能确认这些文件关联或哈希。

缺少语义元数据或个别图片的描述，不得导致基础包无效。已提供但格式错误的语义文件不符合扩展要求，不得被判定为有效语义元数据。基础包与扩展的符合性应分别判定；应用可以因不安全路径或其他安全问题拒绝整个分发包。

符合性不取决于安装目录名称、本地配置、应用界面或算法，也不取决于是否被社区索引收录。
