# AstrBot Meme Pack Index

AstrBot Meme Manager 表情包广场索引仓库。

## 创作自己的表情包

你可以参考示例仓库:

- [示例仓库](https://github.com/anka-afk/astrbot-meme-pack-example)

你可以在表情包管理器的 WebUI 中编辑并在`data/plugin_data/meme_manager/packs/`目录下找到自己编辑好的表情包，将整个目录打包上传到 GitHub 仓库中，并在仓库中添加`manifest.json`文件，示例如下：

```json
{
  "schema_version": 1,
  "id": "your-pack-id",
  "name": "你的表情包名称",
  "version": "1.0.0",
  "description": "这里填写表情包简介（示例：适用于日常聊天的通用表情包）",
  "tags": ["这里填写标签，例如：funny", "anime"],
  "categories": {
    "angry": {
      "description": "示例：当对话包含抱怨、批评或强烈反对时使用（如用户投诉/观点反驳）"
    },
    "baka": {
      "description": "示例：用于轻微责备或吐槽（低级错误/可爱型抱怨），语气保持友善"
    },
    "color": {
      "description": "示例：用于社交场景中的暧昧表达，建议控制使用频率"
    },
    "confused": {
      "description": "示例：用于请求澄清、表达理解障碍，或对用户请求感到困惑时"
    },
    "cpu": {
      "description": "示例：技术讨论中表示思维卡顿（复杂问题/需要加载时间）"
    },
    "fool": {
      "description": "示例：用于自嘲或缓和气氛的幽默场景（小失误/无伤大雅的玩笑）"
    },
    "givemoney": {
      "description": "示例：涉及报酬讨论时使用（服务付费/奖励机制），建议配合明确金额"
    },
    "happy": {
      "description": "示例：用于成功确认、积极反馈或庆祝场景（问题解决/获得成就）"
    },
    "like": {
      "description": "示例：用于表达对事物或观点的喜爱（美食/艺术/优秀方案）"
    },
    "meow": {
      "description": "示例：用于卖萌或萌系互动场景（宠物话题/安抚情绪），慎用于正式场合"
    },
    "morning": {
      "description": "示例：用于早安问候（可按你的业务时区定义时间范围）"
    },
    "reply": {
      "description": "示例：用于等待用户反馈时（提问后/需要确认）"
    },
    "sad": {
      "description": "示例：用于表达伤心、歉意、遗憾或安慰场景（遇到挫折/传达坏消息）"
    },
    "see": {
      "description": "示例：用于表示偷瞄或持续关注（监控进度/观察变化）"
    },
    "shy": {
      "description": "示例：用于涉及隐私话题或收到赞美时（个人故事/外貌评价）"
    },
    "sigh": {
      "description": "示例：用于表达无奈、无语或感慨（重复问题/历史遗留难题）"
    },
    "sleep": {
      "description": "示例：用于作息场景（熬夜/疲劳/休息建议）"
    },
    "surprised": {
      "description": "示例：用于响应超出预期的信息（重大发现/意外转折）"
    },
    "work": {
      "description": "示例：用于工作流程相关场景（任务分配/进度汇报）"
    }
  }
}
```

确保你的仓库中 manifest.json 文件处于仓库根目录，目录层级可以参考[示例仓库](https://github.com/anka-afk/astrbot-meme-pack-example)。

## 可选：为图片添加语义描述

**可以添加，也可以不添加。** 不带语义描述的表情包同样可以安装、分享并提交社区索引，无需为了投稿调用模型或购买语义化服务。

如果已有图片描述，可在包根目录附带 `semantic_metadata.json`，也可以只描述部分图片。推荐通过插件的“分享导出”生成文件，避免携带本机向量和运行状态；可在 manifest 的 `extensions.semantic` 中声明此能力。

字段、版本与可选声明见 [中文协议第 7.5 节](ASTRBOT_MEME_PACK_PROTOCOL_ZH.md#75-可选语义描述扩展) / [English](ASTRBOT_MEME_PACK_PROTOCOL.md#75-optional-semantic-description-extension)，完整样例见 [语义扩展示例](examples/semantic/README.md)。

## 提交社区表情包

如果你需要提交表情包，请使用以下任一方式：

- 会编辑索引文件：提交 PR
- 不会编辑索引文件：提交 Issue（维护者代为添加）

### 提交前准备

1. 准备一个公开可访问的表情包仓库。
2. 确保仓库包含必要内容：
   - manifest
   - memes
   - previews（建议）
3. 确保 source 信息可访问：
   - repo
   - ref
   - subpath
4. 建议先在本地通过“资源广场安装”自测一次。

### 方式一：提交 PR（推荐）

1. Fork 本仓库并创建分支。
2. 按索引格式新增或更新条目。
3. 自检：
   - id 唯一且稳定
   - 字段完整且可解析
   - 预览图与分类描述可用
4. 提交 PR，并使用 PR 模板说明改动。

### 方式二：提交 Issue（不会编辑也可）

1. 新建 Issue。
2. 按 Issue 模板填写包信息与来源仓库。
3. 维护者根据 Issue 补充索引并处理合并。

## 协议与 Schema

- 协议文档参考：[英文](ASTRBOT_MEME_PACK_PROTOCOL.md)/[中文](ASTRBOT_MEME_PACK_PROTOCOL_ZH.md)。
- Schema 参考：`schemas` 目录下的文件。
