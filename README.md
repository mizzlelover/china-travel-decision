# 中国旅行决策助手

让 AI 先弄清你想怎么旅行，再把吃住行玩、预订和临时改线整理成一份路上能查的手机手册。

![中国旅行决策助手：旅行出发](docs/assets/旅行出发封面.png)

**v1.0.2 · 中文旅行规划 Skill · MIT 开源**

适用于中国境内旅行。支持 Codex Skill；另提供 WorkBuddy 原格式安装包，以及可分轮复制到豆包等通用 AI 的[旅游规划提示词](prompts/通用AI_分步旅游规划提示词.md)。

## 攻略看了很多，到了现场还是要重新搜

酒店看起来不错，到了才发现离车站很远；餐厅评分很高，节假日却排不上；行程列满了景点，遇到下雨，只剩一句“灵活调整”。

这个项目把这些问题放进规划流程：先问日期、同行人、预算和体力，再查当期信息，最后把每段移动、每餐、入住和备选接起来。v1.0.2 依据实际试用反馈迭代，重点补充了具名候选、现场操作和 HTML 手册要求。

| 需要解决的事 | 常见一次性泛化提示词容易遗漏 | 本 Skill 的工作要求 |
| --- | --- | --- |
| 这趟旅行适不适合我 | 按热门目的地套路线 | 先分清硬约束、偏好和未知项，再选目的地 |
| 信息现在还有效吗 | 把旧知识当成营业、房态或票价 | 按出行日期调查，留下来源、核验时间和信息状态 |
| 好评值不值得信 | 直接照搬评分和种草 | 看具体门店、体验日期、评论细节、重复转载与商业线索 |
| 长假还能有同样体验吗 | 用平日评价推断假期 | 单独看预约、排队、接驳、餐饮和酒店服务承载 |
| 到底住哪、吃哪、怎么去 | 只有片区和景点名 | 比较具名住宿，给出餐饮分店、菜品和逐段交通 |
| 下雨、闭馆或走不动了 | 只写“视情况调整” | 写清触发条件、下一步、替代地点及如何接回路线 |
| 路上怎么查 | 回翻长聊天记录 | 完整行程默认配单文件、可交互的离线手机 HTML |

认真写出的通用提示词也能实现相似流程。Skill 的便利在于把这些标准长期保存、按任务加载参考，减少每次重新交代；实际质量仍取决于所用模型、当前工具、可访问资料和用户提供的信息。Skill 本身不会给 AI 增加联网或地图权限。

## 你会拿到什么

- **一份有取舍的方案。** 说明为什么适合这组旅客，哪里值得去，哪里需要放弃或错峰。
- **一条接得上的旅途。** 从抵达、入住到每天吃住行玩，再到取行李和返程；关键移动写清起终点、上下车点、时间性质和缓冲。
- **一组能比较的候选。** 住宿看日期、房型、总价、位置和设施；餐饮看具体分店、近期体验、营业与排队；活动看场次、预约和体力要求。
- **一份可随身查的操作手册。** 手机里切换日期、展开地点卡、选择雨天或疲劳备选、勾选准备事项；重要内容在脚本失效时也应可读。

离线 HTML 保存的是已经整理好的信息。实时地图导航、房态、天气、购票和订位仍需要相应在线服务；电话取决于移动信号。页面会标明这些条件。

![手机离线旅行手册概念示意](docs/assets/手机离线手册概念示意.png)

*功能概念示意，实际页面按你的出行需求生成。*

看一份[虚构输出示意](examples/输出示意.md)，了解地点卡、待确认事项和变更方案应写到什么程度。示例不含真实行程或旅行推荐。

## 选一种方式开始

### Codex：安装 Skill

把仓库中的 [`skills/china-travel-decision/`](skills/china-travel-decision/) 文件夹放到你的技能目录，例如 `~/.agents/skills/china-travel-decision/`，保留 `SKILL.md` 和 `references/`。已有同名 Skill 时先比较版本，再决定是否替换。

也可以把这句请求发给 Codex：

```text
请使用 $skill-installer，从 GitHub 仓库 mizzlelover/china-travel-decision
安装 skills/china-travel-decision 目录中的 Skill。
```

安装后在新对话中调用：

```text
请使用 $china-travel-decision 帮我规划一次中国境内旅行。
先了解我的需求，最多问 6 个关键问题，暂时不要排满行程。
完成研究后，请同时给我可保存到手机的离线 HTML 操作手册。
```

### WorkBuddy：选择专用安装包

使用 [`dist/workbuddy-china-travel-decision-v1.0.2.zip`](dist/workbuddy-china-travel-decision-v1.0.2.zip)。它保留原版 WorkBuddy 元数据和引用形式，供支持 Skill 导入的入口使用。这里提供的是发行文件；不表示已经在 WorkBuddy 平台上架。不要用 Codex ZIP 代替它提交。

### 豆包等通用 AI：按五轮推进

打开[通用 AI 分步提示词](prompts/通用AI_分步旅游规划提示词.md)，依次完成需求、研究、行程、HTML、复核。平台不能安装 Skill，也可以按这套流程提问；没有联网或文件能力时，按文中的步骤缩减任务并保留待核实项。

完整步骤见[安装与使用](docs/安装与使用.md)。

## 目录与发行包

```text
skills/china-travel-decision/    Codex 可安装版
targets/workbuddy/china-travel-decision/ WorkBuddy 原格式版
prompts/                        通用 AI 五轮提示词
examples/                       公开的虚构输出示意
docs/                           使用说明与封面
scripts/package_release.py      标准库打包脚本
dist/                           两种独立 ZIP 与 SHA256 校验值
```

安装包用途不同，内部都只包含一个 `china-travel-decision/` 技能目录。Codex 版把版本、作者放在 `metadata` 下，并使用标准 Markdown 引用；WorkBuddy 版保留原格式。两版的旅行决策要求一致。

在仓库根目录运行以下命令即可重新生成发行文件，无需安装 Python 依赖：

```sh
python3 scripts/package_release.py
```

项目地址：[mizzlelover/china-travel-decision](https://github.com/mizzlelover/china-travel-decision)。修改建议欢迎通过 Issue 提交；请使用虚构或脱敏场景，避免公开证件、订单和私人行程。

版本变化见 [CHANGELOG](CHANGELOG.md)，许可见 [MIT LICENSE](LICENSE)。作者：张毅。
