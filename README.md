# Unit Converter Agent

一个使用 OpenAI Agent SDK 构建的最小化单位换算助手示例。示例中提供了一个本地转换工具，利用固定的换算比例支持以下单位：

- 长度：`km`, `m`, `cm`, `mm`, `mile`, `yard`, `foot`, `inch`
- 重量：`kg`, `g`, `lb`, `oz`

核心的换算逻辑在本地执行，不依赖任何外部 API。若提供了 `openai` 包和有效的 API Key，`UnitConverterAgent` 还会自动创建一个可以使用 `convert_units` 工具的 Agent 实例。

## 安装依赖

```bash
pip install openai
```

> 如果只需要命令行换算功能（不调用远端大模型），可以跳过上面的安装。

## 命令行示例

```bash
python -m unit_converter_agent 12 km m
# 输出: 12.0 km = 12000.0 m
```

也可以输出 JSON 结果，方便进一步处理：

```bash
python -m unit_converter_agent 10 lb kg --json
# 输出: {"input": {"value": 10.0, "src_unit": "lb", "tgt_unit": "kg"}, "output": 4.5359237}
```

## 作为库使用

```python
from unit_converter_agent import UnitConverterAgent

agent = UnitConverterAgent()
print(agent.convert(5, "mile", "km"))
```

如果需要结合 OpenAI Agent SDK 的对话流程，可以提供一个 `OpenAI` 客户端：

```python
from openai import OpenAI
from unit_converter_agent import UnitConverterAgent

client = OpenAI()
agent = UnitConverterAgent(client=client)

if agent.agent is not None:
    session = agent.agent.new_session()
    response = session.run("Convert 2.5 kg to lb")
    print(response.output_text)
```

上面的调用会触发远端 Agent 运行 `convert_units` 工具并返回计算结果。
