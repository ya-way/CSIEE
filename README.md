<div align="center">

# CSIEE
### Chinese Student in English Exam

**不会就选 C。三短一长选最长。剩下的交给 Pro Max。**

Zero parameters. Zero API calls. Full confidence.*

[![Tests](https://github.com/ya-way/CSIEE/actions/workflows/ci.yml/badge.svg)](https://github.com/ya-way/CSIEE/actions/workflows/ci.yml)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Parameters 0](https://img.shields.io/badge/parameters-0-brightgreen)
![License MIT](https://img.shields.io/badge/license-MIT-yellow)

[English](README.en.md) · [实测报告](results/personamem-v2/report.md) · [方法说明](docs/methodology.md)

<sub>*信心是梗，准确率看实测。</sub>

</div>

---

你在搭建长期记忆、检索系统和 Agent 工作流。

CSIEE 在数选项有几个字。

这是一个认真做实验的整活项目：把英语考试蒙题口诀写成几行代码，作为选择题 benchmark 的 **option-only baseline**。它不读题、不看聊天历史、不调用大模型，只看选项。

## 产品矩阵

| 版本 | 核心技术 | 参数量 | 读题能力 |
| :-- | :-- | --: | :-- |
| **Lite** | 不会就选 C | 0 | 无 |
| **Pro** | 三短一长选最长，三长一短选最短 | 0 | 依然无 |
| **Pro Max** | 长短口诀 + 数字第三大 + 少选绝对词，投票决定 | 0 | 豪华版的无 |

Lite 的核心算法：

```python
def lite(options):
    return min(2, len(options) - 1)  # C；只有两个选项时选 B
```

Pro 的核心算法：

```python
def pro(options):
    lengths = sorted(len(o.strip()) for o in options)
    if lengths[-1] > 1.5 * lengths[-2]: return longest(options)
    if lengths[1] > 1.5 * lengths[0]: return shortest(options)
    return lite(options)
```

Pro Max 使用固定投票规则，另外提供 `longest`、`shortest`、`numeric`、`cautious` 单规则消融和 `random` 对照。三档名字不代表准确率递增。辅助解析、校验和评测代码当然超过五行，全部见 [strategies.py](csiee/strategies.py)。

## 真跑了：PersonaMem-v2，5,000 题

完整官方文本 benchmark；固定数据版本；seed=42；10 次额外选项打乱。算法未根据本次结果调参。

| 方法 | 准确率 | 打乱选项后平均 | 相对随机期望 |
| :-- | --: | --: | --: |
| 随机期望（解析值） | 25.00% | 25.00% | — |
| 随机实跑 | 24.44% | 25.11% | −0.56 pp |
| CSIEE Lite | 24.68% | 25.22% | −0.32 pp |
| CSIEE Pro | 24.08% | 24.63% | −0.92 pp |
| CSIEE Pro Max | 24.24% | 24.76% | −0.76 pp |
| **永远选最长** | **45.62%** | **45.59%** | **+20.62 pp** |
| 永远选最短 | 23.28% | 23.16% | −1.72 pp |
| 数字第三大 | 24.68% | 25.22% | −0.32 pp |
| 少选绝对词 | 24.28% | 25.02% | −0.72 pp |

**最有效的规则，比 Pro Max 还简单。** 严格的“三短一长”要求长度差超过 1.5 倍；“永远选最长”没有这个门槛，所以二者不是同一个算法。数字规则遇到非纯数字选项会回退到 C。

这个结果提示了一个可检验的选项长度信号，**不代表记忆能力，也不能单凭它宣判 benchmark 无效**。我们采用自己可复现的选项顺序，不是官方评测时的运行顺序；请勿直接把本表与论文里的系统排名拼成榜单。

完整置信区间、顺序敏感性和元数据见 [report.md](results/personamem-v2/report.md)，机器可读汇总见 [summary.json](results/personamem-v2/summary.json)，逐题预测见 [predictions.jsonl](results/personamem-v2/predictions.jsonl)。同一 persona 下的问题可能相关，表中 Wilson 区间不是按 persona 聚类校正的显著性检验。

第二组对照使用 OpenBookQA 完整测试集（500 题），规则保持不变：

| 数据集 | Lite | Pro | Pro Max | 永远选最长 | 最长策略打乱后 |
| :-- | --: | --: | --: | --: | --: |
| PersonaMem-v2 text | 24.68% | 24.08% | 24.24% | 45.62% | 45.59% |
| OpenBookQA test | 26.40% | 28.20% | 28.40% | 36.60% | 36.22% |

两组的随机期望均为 25%。[OpenBookQA 完整报告](results/openbookqa/report.md)保留了所有单规则和随机对照；这是补充实验，不是跨全部 benchmark 的普遍结论。

## 三分钟开跑

需要 Python 3.9+；运行时只用标准库，无 API key、GPU 或模型下载。

```bash
git clone https://github.com/ya-way/CSIEE.git
cd CSIEE
python -m pip install .

csiee guess "10" "40" "20" "30" --strategy numeric
# {"strategy": "numeric", "index": 2, "label": "C", "option": "20"}

csiee eval data/demo.jsonl --seed 42 --shuffles 10
```

不安装也可以在仓库目录内用 `python -m csiee` 替代 `csiee`。`data/demo.jsonl` 是 8 道故意构造的**合成演示题**，只能验证使用流程。

复现真实数据结果：

```bash
csiee download personamem-v2
csiee eval data/raw/personamem-v2.csv --format personamem-v2 --seed 42 --shuffles 10 --output results/local/personamem-v2
```

下载器固定在 revision `ed956dea41521fc4499acbc63f966e0fd3c053ba`，只下载文本题目 CSV，并保存来源及 SHA-256；已有文件不会被覆盖。原始数据不进入 Git。真实数据的下载需要联网；评测本身完全本地运行。

复现 OpenBookQA 对照：

```bash
csiee download openbookqa
csiee eval data/raw/openbookqa.jsonl --format openbookqa --seed 42 --shuffles 10 --output results/local/openbookqa
```

OpenBookQA 来自官方 V1-Sep2018 压缩包，下载器校验固定哈希。感谢 [Mihaylov et al., 2018](https://arxiv.org/abs/1809.02789)。其[数据卡](https://huggingface.co/datasets/allenai/openbookqa)未明确数据许可；原始题目不随本仓库分发，使用时请参照上游条款。

## 打你自己的 benchmark

准备 UTF-8 JSONL，每行一道题。`answer` 是从 **0 开始**的整数索引，`id` 必须唯一：

```json
{"id":"q1","options":["2","8","6","4"],"answer":3}
```

```bash
csiee eval your-benchmark.jsonl --seed 42 --shuffles 10 --output results/local/custom
```

支持 2–26 个选项；拒绝重复选项、越界答案和空数据。每次输出 Markdown 报告、JSON 汇总和逐题预测。`--limit 100` 仅取前 100 题；它不是随机抽样。详细规则和指标说明见 [methodology.md](docs/methodology.md)。

## 开发

```bash
python -m unittest discover -s tests -v
```

测试覆盖答案隔离、选项打乱映射、固定种子、格式校验、指标和 CLI；GitHub Actions 配置了 Windows / Linux、Python 3.9 / 3.12 / 3.14。欢迎提交新的蒙题口诀和有来源的 benchmark adapter，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢与许可

感谢 [PersonaMem-v2 作者](https://github.com/bowen-upenn/PersonaMem-v2)开放数据与代码。[数据集](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2)采用 CC-BY-4.0，论文为 [Jiang et al., 2025](https://arxiv.org/abs/2512.06688)。CSIEE 代码及原创演示采用 [MIT](LICENSE)，不改变上游数据许可。

> 好的 benchmark，值得拥有一个不读题的对照组。
