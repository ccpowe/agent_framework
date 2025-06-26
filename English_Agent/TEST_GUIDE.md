# 测试指南 - LangGraph英语纠错系统

## 📁 测试文件说明

### 测试数据文件

1. **`comprehensive_test.json`** - 综合测试数据集
   - 包含10个类别的测试案例
   - 涵盖所有语法错误类型
   - 基于原始提示词规则生成

2. **`test.json`** - 原始测试数据（参考格式）

### 测试脚本

1. **`test_key_cases.py`** - 关键案例测试
   - 快速验证核心功能
   - 包含你提到的问题案例
   - 适合日常验证

2. **`test_comprehensive.py`** - 综合测试
   - 完整的测试套件
   - 生成详细报告
   - 适合全面评估

3. **`run_fixed_demo.py`** - 交互演示
   - 实时测试功能
   - 用户友好界面
   - 适合手动验证

## 🧪 测试数据分类

### 1. 拼写错误 (spelling_errors)
```json
{
  "input": "My freind is comming to the libary tommorow",
  "expected_output": "My freind[friend] is comming[coming] to the libary[library] tommorow[tomorrow]<.>"
}
```

### 2. 冠词错误 (article_errors)
```json
{
  "input": "I saw a elephant at the zoo",
  "expected_output": "I saw a[an] elephant at the zoo<.>"
}
```

### 3. 复数形式错误 (pluralization_errors)
```json
{
  "input": "I have two cat and three dog",
  "expected_output": "I have two cat[cats] and three dog[dogs]<.>"
}
```

### 4. 大小写错误 (capitalization_errors)
```json
{
  "input": "what is your name",
  "expected_output": "what[What] is your name<.>"
}
```

### 5. 主谓一致错误 (subject_verb_agreement)
```json
{
  "input": "The data suggest different conclusions",
  "expected_output": "The data suggest[suggests] different conclusions<.>"
}
```

### 6. 代词错误 (pronoun_errors)
```json
{
  "input": "Me and him went to the store",
  "expected_output": "Me[I] and him[he] went to the store<.>"
}
```

### 7. 动词形式错误 (verb_form_errors)
```json
{
  "input": "I have went to the store",
  "expected_output": "I have went[gone] to the store<.>"
}
```

### 8. 词性错误 (part_of_speech_errors)
```json
{
  "input": "The medicine will effect your health",
  "expected_output": "The medicine will effect[affect] your health<.>"
}
```

### 9. 虚拟语气错误 (subjunctive_mood)
```json
{
  "input": "If I was rich, I would travel the world",
  "expected_output": "If I was[were] rich, I would travel the world<.>"
}
```

### 10. 标点符号错误 (punctuation_errors)
```json
{
  "input": "What is your name.",
  "expected_output": "What is your name<?>"
}
```

### 11. 结构性问题 (structural_problems)
```json
{
  "input": "Walking down the street, the building looked impressive",
  "expected_output": "{Walking down the street, I found the building looked impressive.}"
}
```

### 12. 混合错误 (mixed_errors)
```json
{
  "input": "hello, my neme are cc ,what is you name？",
  "expected_output": "hello[Hello], my neme[name] are[is] cc, what[What] is you[your] name<?>"
}
```

## 🚀 运行测试

### 快速测试（推荐开始）
```bash
# 使用 uv
uv run python English_Agent/test_key_cases.py

# 或直接运行
python English_Agent/test_key_cases.py
```

### 综合测试
```bash
# 使用 uv
uv run python English_Agent/test_comprehensive.py

# 或直接运行
python English_Agent/test_comprehensive.py
```

### 交互演示
```bash
# 使用 uv
uv run python English_Agent/run_fixed_demo.py

# 或直接运行
python English_Agent/run_fixed_demo.py
```

## 📊 测试报告

### 控制台输出
- 实时显示每个测试案例的结果
- 显示期望输出 vs 实际输出
- 显示通过率和详细反馈

### 详细报告文件
- `test_report.json` - 包含所有测试结果的详细信息
- 可用于进一步分析和调试

## 🎯 标记规则说明

### `[correction]` - 单词替换
- 格式: `original_word[corrected_word]`
- 用于: 拼写、语法、词性错误
- 示例: `what[What]`, `neme[name]`, `are[is]`

### `<correction>` - 标点符号
- 格式: `<punctuation>`
- 用于: 添加或修正标点符号
- 示例: `<.>`, `<,>`, `<?>`, `<!>`, `<;>`

### `{correction}` - 句子重构
- 格式: `{complete_corrected_sentence}`
- 用于: 结构性问题，如悬垂修饰语
- 示例: `{Walking down the street, I found the building impressive.}`

### 无错误情况
- 输出: `✅ No errors found.`

## 🔧 自定义测试

### 添加新测试案例
1. 编辑 `comprehensive_test.json`
2. 在相应类别中添加新案例
3. 运行测试验证

### 创建新测试类别
1. 在JSON中添加新的顶级键
2. 按照现有格式添加测试案例
3. 更新测试脚本（如需要）

## 📈 性能指标

### 通过率标准
- **优秀**: ≥90% 通过率
- **良好**: 70-89% 通过率  
- **需改进**: <70% 通过率

### 迭代次数
- **理想**: 1-2次迭代完成
- **可接受**: 3-4次迭代
- **需优化**: >5次迭代

## 🐛 故障排除

### 常见问题
1. **环境变量未设置**: 检查 `.env` 文件
2. **模块导入失败**: 确认依赖已安装
3. **API调用失败**: 检查网络和API密钥

### 调试技巧
1. 使用 `verbose=True` 查看详细处理过程
2. 检查 `test_report.json` 了解失败原因
3. 单独测试问题案例

## 📝 贡献测试案例

欢迎贡献新的测试案例！请确保：
1. 遵循现有的JSON格式
2. 提供准确的期望输出
3. 覆盖新的错误类型或边界情况