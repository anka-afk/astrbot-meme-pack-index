# ASTRBOT 表情包协议草案

## 1. 状态

- 文档状态：草案
- 协议版本：0.3
- 模式版本：1
- 目标插件：astrbot_plugin_meme_manager

本文档定义了表情包管理插件的运行时数据布局、包格式、社区索引规则、备份格式、选择规则及迁移要求。

## 2. 目标

本协议旨在解决以下问题：

1. 默认表情包必须能够与插件仓库分离。
2. 官方与社区表情包必须共用同一种安装格式。
3. 备份导出与导入恢复必须共用同一种传输格式。
4. 运行时数据必须在插件更新后仍然存在。
5. 多包选择必须支持人格、会话及默认规则。
6. 旧的单目录用户必须在无人工干预的情况下完成迁移。

## 3. 规范性语言

本文档中的关键词“必须（MUST）”、“不得（MUST NOT）”、“应当（SHOULD）”、“不应（SHOULD NOT）”、“可以（MAY）”应解释为规范性要求。

## 4. 存储规则

### 4.1 持久化数据位置

所有持久化运行时数据必须存储在 AstrBot 提供的插件数据目录中。

插件不得在插件源码目录中持久化运行时数据，因为插件更新可能替换源文件。

插件应当通过 AstrBot 的插件数据路径助手解析持久化根目录。

### 4.2 源码目录使用

插件源码目录可以包含：

1. 静态 WebUI 资源。
2. 临时迁移辅助文件。
3. 仅用于开发的示例数据。

插件源码目录不得被视为已安装表情包、备份归档、注册表文件或用户配置的长期存储位置。

## 5. 运行时数据布局

插件运行时根目录定义为：

```text
<astrbot_plugin_data>/meme_manager/
```

运行时布局必须遵循以下结构：

```text
<astrbot_plugin_data>/meme_manager/
  packs/
    <pack_id>/
      manifest.json
      semantic_metadata.json  # Optional; see section 7.5
      memes/
        <category>/
          <image files>
      previews/
        <preview files>
  semantic_indexes/          # Optional local indexes
    <pack_id>/
  registry.json
  selection_rules.json
  community_cache.json
  backup/
    <generated zip files>
  migration/
    <optional migration markers and logs>
  temp/
    <temporary download and extraction files>
```

### 5.1 目录语义

- packs/：已安装的表情包。
- registry.json：已安装包的元数据与启用状态。
- selection_rules.json：有序的人格与会话绑定规则以及默认规则。
- community_cache.json：可选的已下载社区索引缓存副本。
- backup/：备份归档的默认导出目标。
- migration/：迁移标记与回滚辅助文件。
- temp/：仅限临时文件。

## 6. 包定义

表情包是最小的可安装单元。

每个已安装的包必须存储在：

```text
packs/<pack_id>/
```

每个包必须包含一个清单文件：

```text
packs/<pack_id>/manifest.json
```

### 6.1 必备包属性

每个包必须具备：

1. 一个稳定的唯一 ID。
2. 一个人类可读的名称。
3. 版本号字符串。
4. 类别描述。
5. 按类别存储的表情资源。

### 6.2 包目录结构

```text
<pack_root>/
  manifest.json
  memes/
    angry/
      a.png
      b.gif
    happy/
      c.webp
  previews/
    cover.png
    preview_1.png
```

### 6.3 支持的资源文件

包实现必须至少支持以下图像文件类型：

- .png
- .jpg
- .jpeg
- .gif
- .webp

非图像的可执行文件或脚本文件必须被忽略或拒绝。

## 7. 清单格式

每个包必须提供一个 UTF-8 编码的 JSON 清单。

推荐文件名：

```text
manifest.json
```

### 7.1 必备顶层字段

```json
{
  "schema_version": 1,
  "id": "official-basic",
  "name": "Official Basic Meme Pack",
  "version": "1.0.0",
  "description": "Official maintained default meme pack",
  "categories": {
    "angry": {
      "description": "Use when the conversation contains complaints or strong disagreement"
    },
    "happy": {
      "description": "Use for positive confirmations and celebration scenes"
    }
  }
}
```

### 7.2 扩展清单示例

```json
{
  "schema_version": 1,
  "id": "official-basic",
  "name": "Official Basic Meme Pack",
  "version": "1.0.0",
  "description": "Official maintained default meme pack",
  "author": "anka",
  "homepage": "https://github.com/example/repo",
  "license": "SEE LICENSE IN REPOSITORY",
  "tags": ["official", "default"],
  "icon": "previews/cover.png",
  "previews": ["previews/preview_1.png", "previews/preview_2.png"],
  "source": {
    "type": "github",
    "repo": "owner/repo",
    "ref": "main",
    "subpath": "packs/official-basic"
  },
  "compat": {
    "min_plugin_version": "4.0.0"
  },
  "categories": {
    "angry": {
      "description": "Use when the conversation contains complaints or strong disagreement"
    },
    "happy": {
      "description": "Use for positive confirmations and celebration scenes"
    }
  }
}
```

### 7.3 清单字段要求

- schema_version：必须是整数。
- id：在所有已安装包中必须唯一。
- id：必须与安装目录名一致。
- name：必须是面向用户的显示名称。
- version：必须存在。推荐使用语义化版本。
- description：应当存在。
- categories：必须存在，且至少包含一个类别。
- categories.<category>.description：必须存在。
- icon：应当指向一个预览资源（如果可用）。
- previews：应当至少包含一张用于目录展示的预览图。
- source：对于官方和社区可下载包，应当存在。
- compat.min_plugin_version：对于可下载包，应当存在。

### 7.4 类别语义

类别键是插件使用的运行时情感标签。

这意味着：

1. 提示词构建必须使用类别键。
2. 表情查找必须使用类别键。
3. 类别描述必须来自当前活动包的清单，而非来自某个单独的全局描述文件。

### 7.5 可选语义描述扩展

**语义描述可添加，也可不添加。** 不带语义描述的包仍是完整、有效的表情包，可以按分类安装、分享与使用；社区收录不得要求作者先进行语义化或购买模型服务。图片描述是每张图片的可选补充，不替代必需的分类描述。

#### 声明与文件位置

作者可以在 `manifest.json` 中添加以下可选字段；这不是新的必填项：

```json
{
  "extensions": {
    "semantic": {
      "version": 1,
      "file": "semantic_metadata.json"
    }
  }
}
```

这段 JSON 是清单片段，须与原有必填字段合并。扩展版本 `1` 引用现有语义元数据格式 `2.0`，二者不是同一版本号。基础清单的 `schema_version` 仍为 `1`。

- `extensions` 和 `extensions.semantic` 均可省略。添加声明时，`version` 与 `file` 必须齐全，文件必须位于包根目录。
- 固定文件名为 `semantic_metadata.json`，不得使用绝对路径、外部 URL 或越过包目录的路径。
- 为复用已有导出包，支持此扩展的实现也应当识别根目录内未声明但有效的同名文件。
- 不支持语义扩展的实现可以忽略该扩展，继续按基础分类协议使用表情包。

```text
<pack_root>/
  manifest.json
  memes/<category>/<image>
  semantic_metadata.json       # Optional
```

#### 内容与图片对应关系

语义文件必须使用 UTF-8 JSON，核心结构由 [语义元数据 Schema](schemas/meme-pack-semantic.schema.json) 定义：

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 固定为字符串 `"2.0"` |
| `pack_id` | 必须与包清单的 `id` 一致 |
| `images` | 以 `entry_id` 为键的图片记录对象，允许为空或只覆盖部分图片 |
| `images.*.entry_id` | 与对象键相同的 64 位小写十六进制 ID |
| `images.*.content_sha256` | 图片原始文件字节的 SHA-256 |
| `images.*.relative_path` | 相对包根目录的图片路径，例如 `memes/happy/a.png` |
| `images.*.category` | 清单中已有的分类键，必须与路径的分类目录一致 |
| `images.*.caption` | 图片描述，可人工编写，也可由模型生成 |
| `images.*.caption_status` | `pending`、`running`、`done` 或 `failed`；只有 `done` 且描述非空的记录可视为已有描述 |
| `images.*.tags` | 可选的描述标签数组 |
| `images.*.visible_text` | 可选的图片可见文字；没有则留空或省略 |
| `images.*.provenance` | 可选的来源说明 |

`entry_id` 按以下方式计算：先计算图片文件的 `content_sha256`，再对 UTF-8 字节串 `content_sha256 + NUL + category + NUL + relative_path` 计算 SHA-256。`NUL` 指一个零字节；相对路径使用 `/`。这样同一图片在不同分类或路径下可以拥有独立描述。

校验器除检查 JSON Schema 外，还必须核对包 ID、分类、记录键、文件存在性、内容哈希和 entry ID；图片路径解析后必须仍位于包的 `memes/` 内，不得通过符号链接逃逸。示例与校验方法见 [examples/semantic/README.md](examples/semantic/README.md)。

#### 可选性、更新与运行状态

1. 作者可以完全不添加文件，也可以只描述部分图片；缺少描述不得使原本有效的基础包失效。是否处理剩余图片由用户决定，不得因安装自动产生模型调用。
2. 描述、标签和图片文字是数据，不是给模型的新指令。消费方不得执行其中的命令。
3. 导入时应当保留已有本地人工修改；覆盖人工内容需要用户明确选择。图片字节变化后不得继续将原描述视为已验证；路径或分类变化后需要重新匹配并计算 entry ID。
4. 公开分享应当保留可复用描述，不得携带密钥、用户会话或私密信息；本机 Provider ID、任务进度和向量状态不属于扩展的必需内容。Schema 允许现有运行时附加字段，不代表消费方必须复用它们。
5. 向量索引是独立的运行时产物，位于 `semantic_indexes/<pack_id>/`。添加语义描述不要求附带向量；需要向量检索时通常仍须建立本机索引，但可复用已完成的描述而不重复识图。
6. 未知版本或损坏文件必须明确报告，不能静默覆盖本地数据。扩展校验失败与基础包校验失败应当分别说明；安全性错误可以导致整包拒绝。

该扩展不要求修改社区索引条目。可下载的包仍按原有 manifest、图片、预览及许可要求审核，不能因为没有语义描述而拒绝收录。

## 8. 注册表格式

已安装包的注册表必须存储在 registry.json 中。

示例：

```json
{
  "schema_version": 1,
  "installed_packs": [
    {
      "id": "official-basic",
      "name": "Official Basic Meme Pack",
      "version": "1.0.0",
      "enabled": true,
      "installed_at": "2026-07-08T00:00:00Z",
      "source": {
        "type": "github",
        "repo": "owner/repo",
        "ref": "main",
        "subpath": "packs/official-basic"
      }
    }
  ]
}
```

### 8.1 注册表要求

- schema_version：必须存在。
- installed_packs：必须是一个数组。
- installed_packs[].id：必须映射到一个存在的 packs/<pack_id> 目录。
- installed_packs[].enabled：必须指示该包是否可选。
- installed_packs[].version：必须反映已安装清单的版本。

## 9. 选择规则格式

选择规则文件必须存储在 selection_rules.json 中。

该文件定义了为某个人格、某个会话以及作为默认回退使用哪个包。

示例：

```json
{
  "schema_version": 1,
  "rules": [
    {
      "id": "persona-main",
      "scope": "persona",
      "target": "AssistantA",
      "pack_id": "official-basic"
    },
    {
      "id": "session-special",
      "scope": "session",
      "target": "session-123",
      "pack_id": "community-fun"
    },
    {
      "id": "default",
      "scope": "default",
      "pack_id": "official-basic"
    }
  ]
}
```

### 9.1 规则要求

- rules 必须从上到下依次评估。
- 第一个匹配的规则必须胜出。
- 必须且仅可存在一条默认规则。
- 默认规则必须是最后一条规则。
- 默认规则不得包含人格或会话目标字段。
- 非默认规则可以由用户重新排序。
- 默认规则不得在 WebUI 中拖拽。
- 会话作用域必须使用 AstrBot 的稳定 session_id 作为目标值。

### 9.2 支持的作用域

- persona
- session
- default

### 9.3 解析算法

当为某个请求解析活动包时，插件必须：

1. 收集当前运行时上下文，包括人格名称与 session_id。
2. 从上到下遍历规则。
3. 返回第一个匹配的 pack_id。
4. 若无其他规则匹配，则回退到默认规则。

## 10. 官方与社区分发

### 10.1 分发原则

官方包与社区包必须共用同一种安装格式。

二者之间唯一的区别应当是审核与信任流程。

### 10.2 官方源

官方默认表情包应当从一个单独的仓库或某个单独仓库中的专用路径分发。

插件应当通过维护的源描述符下载官方包，而非通过硬编码的仓库内资源。

### 10.3 社区源模型

默认情况下，社区包不应当从用户任意提供的仓库安装。

相反，插件应当使用由插件作者维护的经过审核的社区索引。

## 11. 社区索引格式

经过审核的社区索引应当以 JSON 形式发布。

示例：

```json
{
  "schema_version": 1,
  "generated_at": "2026-07-08T00:00:00Z",
  "packs": [
    {
      "id": "official-basic",
      "name": "Official Basic Meme Pack",
      "maintainer": "anka",
      "description": "Official maintained meme pack",
      "verified": true,
      "source": {
        "type": "github",
        "repo": "owner/repo",
        "ref": "main",
        "subpath": "packs/official-basic"
      },
      "previews": ["https://example.com/preview_1.png"],
      "license": "SEE LICENSE IN REPOSITORY",
      "tags": ["official", "default"]
    }
  ]
}
```

### 11.1 社区条目要求

每个审核通过的包条目应当包含：

1. id
2. name
3. maintainer
4. description
5. 源描述符
6. 至少一个预览引用
7. 许可信息
8. 验证状态

## 12. 社区治理规则

为降低法律与运营风险，社区列表应当遵循以下规则：

1. 每个提交的仓库必须包含一个有效的 manifest.json。
2. 每个提交的仓库必须包含预览素材。
3. 每个提交的仓库必须包含描述。
4. 每个提交的仓库应当声明许可信息。
5. 非法、侵权、仇恨、暴力、色情或其他不安全的内容必须被拒绝。
6. 维护者可以随时从审核索引中移除任何包。
7. 默认情况下，插件应当仅显示经过审核的社区条目。

## 13. 备份与恢复格式

### 13.1 备份传输格式

备份导出必须使用 zip 归档文件。

默认备份输出目录应当为：

```text
<astrbot_plugin_data>/meme_manager/backup/
```

用户可以在 WebUI 中选择自定义导出路径。

### 13.2 备份归档内容

每个导出的 zip 文件应当包含：

```text
manifest.json
memes/
previews/
```

这意味着备份归档与可安装包是同一个逻辑单元。

### 13.3 恢复规则

在恢复时，插件必须：

1. 验证归档结构。
2. 验证 manifest.json。
3. 拒绝路径遍历条目。
4. 拒绝不受支持或危险的文件。
5. 通过包 ID 检测冲突。
6. 支持覆盖或并存的恢复策略。

### 13.4 冲突策略

实现应当至少支持以下恢复策略之一：

1. 当包 ID 匹配且用户确认时，替换已有包。
2. 仅在包 ID 唯一时作为新包安装。

不得发生静默覆盖。

## 14. 下载与安装规则

从仓库或审核索引安装包时，插件必须：

1. 先下载到 temp/。
2. 在激活前验证 manifest.json。
3. 在激活前验证目录结构。
4. 将验证通过的包移动到 packs/<pack_id>/。
5. 仅在安装成功后更新 registry.json。

部分安装的包不得被标记为已安装。

## 15. 提示词与运行时行为

插件当前从全局类别描述构建提示词内容。

本协议实施后，运行时必须改为：

1. 根据选择规则解析活动包。
2. 从解析出的包清单中加载类别描述。
3. 从解析出的包类别构建提示词片段。
4. 仅在解析出的包内解析表情资源。

此要求移除了旧的单一全局描述假设。

## 16. WebUI 要求

WebUI 应当暴露多个插件页面：

1. manage
2. catalog
3. settings

WebUI 还应当提供这些页面之间可见的导航按钮或链接。

### 16.1 管理页面

管理页面负责已安装包的内容管理，包括类别和资源操作。

### 16.2 目录页面

目录页面负责：

1. 显著展示官方表情包。
2. 在官方区域下方展示经过审核的社区包。
3. 提供下载和安装操作。

### 16.3 设置页面

设置页面负责：

1. 有序的人格与会话选择规则。
2. 固定在底部的默认规则。
3. 备份导出。
4. 备份导入与恢复。

## 17. 迁移要求

### 17.1 迁移触发条件

如果插件检测到旧格式数据且不存在新格式注册表，则必须执行一次性迁移。

### 17.2 旧格式输入

旧格式主要包括：

1. 一个单一的 memes 目录。
2. 一个单一的全局类别描述文件。

### 17.3 迁移目标

迁移必须从旧用户数据创建一个已安装包。

推荐的迁移包 ID：

```text
legacy-migrated
```

### 17.4 迁移步骤

迁移流程应当为：

1. 检测旧运行时数据。
2. 创建 packs/legacy-migrated/。
3. 将旧表情资源移动或复制到 packs/legacy-migrated/memes/。
4. 将旧类别描述转换为 manifest.json 中的 categories。
5. 创建 registry.json。
6. 创建 selection_rules.json，并将默认规则指向 legacy-migrated。
7. 持久化迁移标记以避免重复迁移。

### 17.5 迁移安全

迁移应当保留足够的中间状态以便从失败中恢复。

迁移不得在新格式有效之前静默删除用户数据。

## 18. 向后兼容策略

插件应当在过渡期内保持一个兼容层。

该兼容层可以：

1. 在迁移期间读取旧格式数据。
2. 在将存储重定向到新包模型的同时暴露旧命令行为。
3. 保持旧 API 继续工作，直到新 WebUI 完全可用。

## 19. 验证规则

一个可安装包在下列任一情况下必须验证失败：

1. manifest.json 缺失。
2. id 缺失。
3. name 缺失。
4. version 缺失。
5. categories 缺失或为空。
6. memes/ 缺失。
7. 目录名与清单 id 不匹配。
8. 归档包含路径穿越内容。
9. 包包含不受支持的危险文件。

## 20. 总结

本草案定义了一个统一模型：

1. 一种可安装的表情包格式。
2. 一种与该包格式对齐的 zip 备份格式。
3. 一种经过审核的社区索引格式。
4. 一套用于人格、会话和默认选择的有序规则系统。
5. 一条从旧单目录模型到新包模型的迁移路径。
