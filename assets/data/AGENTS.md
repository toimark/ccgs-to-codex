# 数据文件规则（路径范围 AGENTS.md）

完整规则：[../../.claude/rules/data-files.md](../../.claude/rules/data-files.md)

在编辑本目录（`assets/data/**`）下任何文件时，必须遵循：

- 所有 JSON 必须合法；损坏的 JSON 会阻塞构建管线。
- 文件命名小写 + 下划线，遵循 `[system]_[name].json`。
- 每个数据文件需有文档化 schema（JSON Schema 或对应设计文档说明）。
- 数值附带注释或配套文档说明含义。
- JSON 内部键名使用 camelCase。
- 不允许孤立条目；每个条目必须被代码或其他数据文件引用。
- 破坏性 schema 变更需对数据文件版本化。
- 可选字段需提供合理默认值。
