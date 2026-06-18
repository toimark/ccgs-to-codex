# 着色器规则（路径范围 AGENTS.md）

完整规则：[../../.claude/rules/shader-code.md](../../.claude/rules/shader-code.md)

在编辑本目录（`assets/shaders/**`）下任何文件时，必须遵循：

- 文件命名 `[类型]_[类别]_[名称].[扩展名]`；以着色器类型为前缀（`spatial_`、`canvas_`、`particles_`、`post_`）。
- 所有 uniform / 参数需有描述性名称与适当 hints；相关参数分组（Godot `group_uniforms`、Unity `[Header]`、Unreal Category）。
- 文件顶部包含作者与用途注释；非显而易见的数学密集计算需注释。
- 禁止魔法数字；使用命名常量或文档化 uniform。
- 记录目标平台与复杂度预算；移动端非必须处使用 `half`/`mediump`。
- 减少片元着色器纹理采样；避免动态分支，改用 `step()`、`mix()`、`smoothstep()`。
- 循环内不做纹理读取；模糊用两遍处理（先水平后垂直）。
- 在最低规格目标硬件上测试；为低质量级别提供 fallback；不混用不同渲染管线的着色器。
- 减少变体数量；记录所有 keyword / variant 用途；尽量做特性剥离。
