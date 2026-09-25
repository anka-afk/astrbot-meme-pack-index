# AstrBot Meme Pack Specification

[中文版](ASTRBOT_MEME_PACK_PROTOCOL_ZH.md)

- Document revision: 0.3
- Manifest schema version: `1`
- Optional semantic extension version: `1`
- Semantic metadata schema version: `"2.0"`

## 1. Scope

This specification defines the portable contents of an AstrBot meme pack: its directory structure, manifest, category assets, previews, and optional semantic descriptions. It applies equally to official, community, and privately distributed packs.

It does not define application storage locations, installed-pack registries, persona or session selection, prompts, retrieval algorithms, model calls, WebUI layouts, download or installation procedures, backup management, or migration behavior. Community indexing and admission are repository policies documented in the [README](README.md#社区索引格式与收录要求), not conditions for pack-format conformance.

Revision 0.3 replaces the implementation-oriented scope of revision 0.2. It does not change the existing JSON schemas or their version numbers. A pack's identity comes from its manifest, independently of its containing directory name.

## 2. Terminology and requirements

- **Pack root**: the directory containing `manifest.json` and `memes/`.
- **Manifest**: the UTF-8 JSON object describing the pack in `manifest.json`.
- **Category**: a named group of images with a description in the manifest.
- **Base pack**: the manifest and category assets, without requiring any extension.
- **Semantic extension**: optional per-image descriptions associated with specific image files.

**MUST** and **MUST NOT** express mandatory requirements. **SHOULD** and **SHOULD NOT** express recommendations that may be departed from for a justified reason. **MAY** expresses an option. Examples are informative; field constraints and conformance requirements are normative.

The [manifest schema](schemas/meme-pack-manifest.schema.json) and [semantic metadata schema](schemas/meme-pack-semantic.schema.json) define JSON types, allowed properties, lengths, and patterns. The corresponding document MUST satisfy its schema. The file relationships and content checks specified below apply in addition to JSON Schema validation.

## 3. Pack structure

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

`manifest.json` and `memes/` MUST exist at the pack root. `previews/` and `semantic_metadata.json` are optional. The root directory MAY have any name and MAY be a repository root or a subdirectory; it need not match the manifest `id`.

Meme assets MUST be stored as `memes/<category>/<image>`. The category directory name MUST match the corresponding manifest category key exactly. This specification does not prescribe a fixed vocabulary of categories.

A pack MAY include supporting documents such as a README, license, or attribution file. Such documents are not meme assets and do not replace manifest fields.

## 4. Manifest

### 4.1 Required fields

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_version` | integer | MUST be `1` |
| `id` | string | Stable pack identifier, 2–64 characters, matching `^[a-z0-9][a-z0-9._-]{1,63}$` |
| `name` | string | Display name, 1–128 characters |
| `version` | string | Pack release identifier, 1–64 characters; semantic versioning is RECOMMENDED |
| `categories` | object | At least one category; each value MUST contain `description` |

A pack ID SHOULD remain unchanged across releases and SHOULD distinguish the pack from other published packs. The pack's `version` identifies its content release; it is independent of document, schema, and extension versions.

Category keys MUST match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`. Each category value MUST be an object containing a `description` string of 1–2000 characters. The description SHOULD explain the category's meaning or intended use. It does not prescribe how an application constructs prompts or chooses images.

### 4.2 Optional fields

Optional fields MAY be omitted. When present, they MUST meet the following constraints and the manifest schema.

| Field | Type | Meaning and constraints |
| --- | --- | --- |
| `description` | string | Pack description, 1–2000 characters; RECOMMENDED |
| `author` | string | Author or attribution label, 1–128 characters |
| `homepage` | string | Homepage URI, at most 2048 characters |
| `license` | string | License identifier or reference to licensing information, 1–256 characters; RECOMMENDED |
| `tags` | array of strings | At most 32 unique tags, each 1–64 characters |
| `icon` | string | Pack-relative image path, 1–512 characters |
| `previews` | array of strings | At most 32 unique pack-relative image paths, each 1–512 characters |
| `source` | object | Source descriptor defined in section 4.3 |
| `compat` | object | MAY contain `min_plugin_version`, a string of 1–64 characters describing the minimum compatible meme-manager plugin version |
| `extensions` | object | Optional extension declarations; the semantic declaration is defined in section 6 |

An icon and previews SHOULD be supplied for display purposes. Their absence does not invalidate a base pack. The manifest does not allow additional top-level properties; extension declarations belong under `extensions`, which permits additional extension names. Unknown extension names do not establish portable behavior under this specification.

### 4.3 Source descriptor

If `source` is present, all four fields below MUST be present. The descriptor identifies the pack's source; it does not require a particular download or installation workflow.

| Field | Requirement |
| --- | --- |
| `type` | The string `"github"` |
| `repo` | Repository in `owner/repo` form, matching `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`, at most 200 characters |
| `ref` | Nonempty branch, tag, or commit reference, at most 200 characters |
| `subpath` | Repository-relative pack root, 1–512 characters; use `"."` for the repository root |

`subpath` MUST satisfy the schema's relative-directory-path constraints. It MUST NOT be an absolute path, contain backslashes or `..`, or resolve outside the repository.

### 4.4 Minimal manifest example

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

This example needs only `manifest.json` and category assets under `memes/happy/`. Neither preview fields nor semantic metadata are required.

### 4.5 Extended manifest example

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

The referenced preview and declared semantic metadata file MUST exist. The latter MUST satisfy section 6 for this pack's ID and image files.

## 5. Image resources and paths

The base image formats are PNG (`.png`), JPEG (`.jpg`, `.jpeg`), GIF (`.gif`), and WebP (`.webp`). These formats apply to meme assets and previews. Other image formats are outside the interoperability guarantees of this specification.

Pack-relative asset paths MUST use `/` separators and refer to existing files within the pack root. They MUST NOT be absolute paths, external URLs, or paths that escape the pack root, including through symbolic links. Manifest `icon` and `previews` paths MUST also satisfy the schema, which disallows backslashes and any `..` substring. Semantic image paths have the more specific structure defined in section 6.

Previews SHOULD be placed in `previews/`. They illustrate the pack and do not constitute a category unless separately included as assets under `memes/` and declared in `categories`.

Executable files and scripts are not image resources and MUST NOT be treated as meme assets. A pack's descriptions and other metadata are data; they do not authorize command execution.

## 6. Optional semantic descriptions

<a id="75-optional-semantic-description-extension"></a>

### 6.1 Optionality and declaration

A base pack remains complete without semantic metadata. A semantic file MAY describe any subset of the pack's images, including none. Per-image descriptions supplement the required category descriptions.

The optional `extensions.semantic` declaration MUST contain `version: 1` and `file: "semantic_metadata.json"`, with no additional properties. If declared, that file MUST exist at the pack root. A valid file with this fixed name MAY also be supplied without a declaration, for compatibility with existing exports.

The file MUST be a UTF-8 JSON object conforming to the [semantic metadata schema](schemas/meme-pack-semantic.schema.json). Extension version `1`, metadata schema version `"2.0"`, and manifest schema version `1` are separate identifiers.

### 6.2 Metadata fields

| Field | Requirement |
| --- | --- |
| `schema_version` | The string `"2.0"` |
| `pack_id` | MUST equal the manifest `id` |
| `images` | Object keyed by `entry_id`; empty and partial coverage are permitted |
| `images.*.entry_id` | 64 lowercase hexadecimal characters; MUST equal the record key |
| `images.*.content_sha256` | SHA-256 digest of the image's original file bytes, as 64 lowercase hexadecimal characters |
| `images.*.relative_path` | Path of an existing image in the form `memes/<category>/<filename>`, with `/` separators and no extra directory level |
| `images.*.category` | Existing manifest category key, matching the path's category component exactly |
| `images.*.caption` | Description string; MAY be empty unless `caption_status` is `done` |
| `images.*.caption_status` | One of `pending`, `running`, `done`, or `failed`; `done` requires a caption containing a non-whitespace character |
| `images.*.tags` | Optional array of unique strings |
| `images.*.visible_text` | Optional string containing text visible in the image |
| `images.*.provenance` | Optional string describing the description's source |

All fields above except `tags`, `visible_text`, and `provenance` are required. `caption_status` retains the existing format's values; it does not prescribe a processing workflow.

### 6.3 Image identity

`entry_id` MUST be the lowercase hexadecimal SHA-256 digest of the UTF-8 encoding of:

```text
content_sha256 + NUL + category + NUL + relative_path
```

`NUL` is one zero byte. The formula uses the exact stored category and relative path. Identical bytes at different paths or in different categories therefore have different entry IDs.

The content hash MUST match the referenced file. The record key, `entry_id`, and computed entry ID MUST agree. The resolved image path MUST remain within the pack's `memes/` directory, including after resolving symbolic links. Changes to the image bytes, category, or relative path require the corresponding identity fields and record key to be updated.

A complete fixture with a real image, matching hashes, and validation instructions is available in [examples/semantic](examples/semantic/README.md).

### 6.4 Portable content

Descriptions MAY be written by people or generated by models; the format requires neither a model service nor a vector index. Publicly distributed metadata MUST NOT contain credentials, private conversations, or private information.

The semantic schema accepts additional properties for compatibility with existing files. Such properties do not establish portable semantics. Local provider identifiers, processing progress, and vector state are not required pack content. Applications may use the base pack without supporting semantic descriptions.

## 7. Distribution boundaries

A pack MAY be distributed as a directory, a repository subtree, or files in an archive. Its portable content is the pack root and its contents defined above. Repository or archive wrapper directory names are not pack identifiers.

If an archive carries a pack, its entries MUST NOT resolve outside the extraction root. This specification does not define an archive container version, require a particular compression format, or specify application backup and restore behavior.

Publication, community admission, licensing review, and installation are separate from conformance to this data format. Community requirements are maintained in the [README](README.md#社区索引格式与收录要求).

## 8. Conformance

Base-pack validation consists of the following checks:

1. The pack root contains a readable UTF-8 JSON `manifest.json` and a `memes/` directory.
2. The manifest satisfies the manifest schema, including required fields and category descriptions.
3. Meme assets follow `memes/<category>/<image>`, with category names matching the manifest.
4. Referenced icons and previews exist, and image resources and paths satisfy section 5.

Semantic-extension validation additionally checks the declaration and file, schema version, pack ID, category membership, record keys, file existence, content hashes, and entry IDs as defined in section 6. JSON Schema validation alone does not check these file relationships or hashes.

Absence of semantic metadata or descriptions for individual images MUST NOT invalidate a base pack. A malformed supplied semantic file does not conform to the extension and MUST NOT be reported as valid semantic metadata. Base-pack and extension conformance are separate results; an application may reject an entire distribution for unsafe paths or other security failures.

Conformance does not depend on an installed directory name, local configuration, an application's interfaces or algorithms, or acceptance into a community index.
