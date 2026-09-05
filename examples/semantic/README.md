# 可选语义扩展示例 / Optional semantic extension example

`optional-semantic-demo/` 是一个含占位 PNG 的协议测试包，演示图片哈希、entry ID 和描述文件的对应关系，不是推荐的聊天表情资源。

The fixture contains a placeholder PNG to demonstrate file hashes, entry IDs and metadata. It is not intended as a useful chat sticker pack.

- 不使用语义扩展时，删除 `semantic_metadata.json` 和 manifest 的 `extensions` 字段即可，基础表情包仍完整有效。
- 可以只为部分图片提供记录，剩余图片照常按分类使用。
- 元数据版本为 `2.0`，可选清单扩展版本为 `1`，基础清单版本为 `1`。
- 使用插件编辑的语义描述时，优先通过“分享导出”生成可分发文件。

Omit both the metadata file and the optional manifest declaration for a plain category pack. Partial image coverage is valid. Metadata version `2.0`, extension version `1`, and manifest schema version `1` are separate identifiers.

从仓库根目录验证 / Validate from the repository root:

```sh
python -m pip install jsonschema
python -m unittest discover -s tests -v
```

校验包含未添加扩展、完整扩展、部分覆盖、非法路径和版本，以及示例图片的实际内容哈希和 entry ID。
