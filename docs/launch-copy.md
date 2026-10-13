# 小红书发布文案草稿

标题：我用几行蒙题口诀，做了一个「零参数大模型」

我做了个 GitHub 项目：CSIEE —— Chinese Student in English Exam。

它不看题，不看上下文，不调 API。

- Lite：不会就选 C。
- Pro：三短一长选最长，三长一短选最短。
- Pro Max：数字第三大 + 排除绝对词 + 口诀投票。

算法很短，解释实验怎么做的文档倒是写了挺长。

我接上了 PersonaMem-v2 的真实选择题数据，也做了选项打乱对照。具体成绩看仓库里的实测表；Pro Max 不保证比 Lite 强，毕竟玄学也要接受消融实验。

这个项目想问的是：如果只看选项就能猜中一些题，分数里有多少来自能力，有多少来自出题格式？一次实验不能直接给 benchmark 判死刑，但可以多放一个很便宜的对照组。

仓库：https://github.com/ya-way/CSIEE

#开源项目 #AI #程序员 #大模型 #GitHub #整活

---

发布提示：最终数字以 `results/personamem-v2/report.md` 为准。不要把 demo 分数当真实结果，也不要把 option-only 分数说成记忆系统能力。这是文案草稿，尚未发布到任何社交平台。
