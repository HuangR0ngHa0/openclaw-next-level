---
name: xiaohongshu-search
description: >
  在小红书上搜索指定关键词，自动过滤广告和无效内容，
  总结有价值的帖子，并可将结果同步到飞书多维表格。
  触发词：小红书搜索、搜小红书、小红书上查、红书上找
---

# 小红书内容搜索与分析 Skill

## 目标

把“小红书搜索 → 结果页结构化提取 → 详情页稳定进入 → 正文与评论提取 → 过滤与评分 → 报告与飞书同步”固定成可复用流程。

本 Skill 的核心不是“盲点页面元素”，而是：
- 优先复用 **OpenClaw browser + `profile=user`**
- 对小红书搜索结果页做 **DOM 结构化提取**
- 对详情页进入做 **主路径 + 兜底路径 + 成功验收 + 失败分类**
- 对正文抓取优先使用 **DOM evaluate**，而不是只依赖 snapshot
- 对批量执行加入 **节奏控制、失败记录和风控约束**

适用场景：
- 搜索某个话题在小红书上的真实讨论、经验、教程、踩坑
- 过滤广告、搬运、引流和低价值内容
- 提取值得看的帖子与关键信息
- 结果同步到飞书消息或 Feishu Bitable

---

## 运行前检查

### 1. 浏览器接入必须先通

优先使用：`browser` 工具 + `profile="user"` + `target="host"`

执行前先检查：
1. `browser action="status" profile="user" target="host"`：确认连接正常
2. `browser action="tabs" profile="user" target="host"`：确认可以看到真实标签页
3. 若为 Ubuntu + Chromium，优先使用 **remote CDP** 模式，而不是不稳定的 existing-session 自动接管

### 2. 建议的浏览器接入方式

在当前用户环境中，验证更稳定的方案是：
- 手工启动 Chromium 并启用 remote debugging
- OpenClaw 使用 `browser.profiles.user.cdpUrl` 连接到该浏览器

示例配置思路：

```json5
browser: {
  enabled: true,
  noSandbox: true,
  executablePath: "/snap/bin/chromium",
  defaultProfile: "user",
  profiles: {
    user: {
      cdpUrl: "http://127.0.0.1:9222",
      color: "#00AA00"
    }
  }
}
```

### 3. 登录态检查

必须复用用户已登录的小红书浏览器会话。

若页面出现以下情况之一，停止自动化并提示用户先手动处理：
- 登录页 / 扫码页
- 空白页
- 验证码 / 风控页
- 明显页面异常，导致正文无法加载

---

## 参数提取

从用户输入中提取：
- `keyword`：搜索关键词，必填
- `max_posts`：最多分析帖子数，默认 `8`，建议上限 `15`
- `filter_mode`：`strict | normal | loose`，默认 `normal`
- `save_to_bitable`：是否写入 Feishu Bitable，默认 `false`
- `send_feishu_notice`：是否发送结果汇报，默认 `true`

### 建议默认值
- 首轮候选抽取：`8-12`
- 首轮详情深挖：`3-5`
- 单次会话中详情页最大尝试数：`<= 10`

默认不要一次深挖太多详情页，避免风控。

### 轻量执行模式（推荐默认）

如果用户没有特别要求“尽量全量”，默认启用轻量模式：
- 只抽取前 `8` 条候选
- 只深挖前 `3` 条详情
- 每条最多抓 `3` 条评论样本
- `body_text` 截断到 `1500-2500` 字
- 一旦连续失败达到阈值，立即暂停并汇报

轻量模式的目标是：
- 降低 token 消耗
- 降低浏览器交互次数
- 降低风控概率
- 先验证结果质量，再决定是否扩量

### 建议的最小字段规范

#### 结果项 ResultItem

```json
{
  "note_id": "69b4ee7d0000000022002dd8",
  "detail_url": "https://www.xiaohongshu.com/explore/69b4ee7d0000000022002dd8",
  "search_wrapper_url": "https://www.xiaohongshu.com/search_result/69b4ee7d0000000022002dd8?...",
  "author_name": "DobbyAi",
  "author_profile_url": "https://www.xiaohongshu.com/user/profile/...",
  "position": 5,
  "extract_confidence": "high"
}
```

#### 详情结果 DetailResult

```json
{
  "note_id": "69b4ee7d0000000022002dd8",
  "detail_status": "SUCCESS",
  "detail_failure_type": "",
  "attempt_path": "WRAPPER",
  "success_signals": ["HAS_TITLE", "HAS_AUTHOR", "HAS_BODY", "HAS_COMMENTS"],
  "title": "20 个最靠谱神级 🦞Skill",
  "author": "DobbyAi",
  "desc": "...",
  "body_text": "...",
  "comment_samples": ["...", "...", "..."]
}
```

#### 失败记录 FailureRecord

```json
{
  "note_id": "699e9e910000000015031d9f",
  "final_status": "FAILED",
  "attempts": [
    {"path": "WRAPPER", "result": "FAILED", "failure_type": "DETAIL_ABORTED"},
    {"path": "DETAIL", "result": "FAILED", "failure_type": "DETAIL_ABORTED"}
  ],
  "remark": "包装与裸详情均被站点中断"
}
```

### 失败分类枚举（固定）

为避免后续执行时自由发挥，失败类型固定为：
- `DETAIL_ABORTED`
- `DETAIL_REDIRECTED_TO_PROFILE`
- `DETAIL_RENDER_EMPTY`
- `DETAIL_RISK_OR_LOGIN`
- `DETAIL_UNKNOWN_ERROR`
- `RESULT_UNUSABLE`

---

## 执行流程

## 第一步：打开搜索页

优先方式：
1. `navigate` 到：
   `https://www.xiaohongshu.com/search_result?keyword=<keyword>`
2. 若站点自动改写 query 参数或增加 `type=`，允许保留
3. 若直链结果页不稳定，则：
   - 打开首页
   - 定位搜索框
   - 输入关键词
   - 提交搜索

### 搜索成功信号
满足任一即可继续：
- 页面标题包含“小红书搜索”
- URL 包含 `/search_result`
- DOM 中出现搜索结果卡片结构

---

## 第二步：结果页结构化提取

**不要只靠 snapshot 的 ref 猜卡片。**
优先使用 `evaluate` 从 DOM 里提取所有 `a[href]`，并按链接类型分类。

### 结果页常见链接类型

#### A. 裸详情链接
```text
/explore/<id>
```

#### B. 搜索结果包装链接
```text
/search_result/<id>?xsec_token=...&xsec_source=...
```

#### C. 作者主页链接
```text
/user/profile/<id>
```

### 结果项建模

每条候选结果尽量提取成结构：
- `note_id`
- `detail_url`：`/explore/<id>`
- `search_wrapper_url`：若存在 `/search_result/<id>?...`
- `author_name`
- `author_profile_url`
- `card_class`
- `position`
- `extract_confidence`：高 / 中 / 低

### 重要规则
- **作者主页链接不能当详情页入口**
- 包装链接和裸详情链接都保留，供后续多级尝试
- 若无法稳定提取标题，允许先只拿作者 + note_id + url，后续到详情页补标题
- 如果某条候选既没有包装链接也没有裸详情，直接标记为 `RESULT_UNUSABLE`

---

## 第三步：首轮过滤

列表页阶段先过滤明显低价值内容：
- 用户主页误入口
- 明显非帖子链接
- 重复 note_id
- 营销/商业导向明显但标题信息极少的结果
- 看起来明显不属于目标话题的结果

此阶段不做最终广告判断，只做粗筛。

### 首轮过滤输出结构

```json
{
  "note_id": "...",
  "author_name": "...",
  "detail_url": "...",
  "search_wrapper_url": "...",
  "prefilter_status": "KEEP|DROP",
  "prefilter_reason": "DUPLICATE|PROFILE_ONLY|LOW_SIGNAL|OFF_TOPIC|OK"
}
```

---

## 第四步：详情页进入稳定器（核心）

这是本 Skill 最关键的一层。

### 为什么需要稳定器
小红书详情页进入不稳定，常见原因包括：
- 搜索结果不是普通静态列表，而是前端路由 + 动态状态页
- 直接 `goto /explore/<id>` 不总是等价于真实用户点击
- 部分帖子依赖搜索结果包装态或 token
- 页面自身可能有脚本错误、资源错误、mixed content、风控或特殊内容类型差异

因此，**不能把单一进入方法当成长期稳定方案。**

### 详情进入顺序
对每条候选帖子，按以下顺序尝试：

#### 主路径：包装链接优先
如果存在 `search_wrapper_url`，先尝试：
```text
/search_result/<id>?xsec_token=...
```

原因：
- 更接近用户真实点击搜索结果卡片的路径
- 通常比裸 `/explore/<id>` 更符合站点预期

#### 兜底路径：裸详情链接
如果包装链接失败，再尝试：
```text
/explore/<id>
```

#### 第二兜底：真实点击交互
如果上述两种路径都不稳定，但该结果高度相关，可尝试：
- 回到搜索结果页
- 精确点击卡片区域中对应的 `cover mask` / 包装区域
- 避免点击作者名或主页入口

#### 最终降级：标记失败
若仍失败，不要假装成功，应记录为：
- `DETAIL_ABORTED`
- `DETAIL_REDIRECTED_TO_PROFILE`
- `DETAIL_RENDER_EMPTY`
- `DETAIL_RISK_OR_LOGIN`
- `DETAIL_UNKNOWN_ERROR`

---

## 第五步：详情页成功验收

进入详情页后，**不能只看 URL**。
必须做成功验收。

### 详情成功信号
满足以下至少 2 项，才算成功进入详情页：
- `document.title` 不再是搜索页标题
- 能抓到标题（如 `h1` / `.title`）
- 能抓到作者名
- bodyText 中出现正文段落
- bodyText 中出现“共 X 条评论”或评论用户名
- URL 为 `/explore/<id>` 或 note detail 相关结构

### 详情失败信号
满足以下任一项，应视为失败或异常：
- 页面仍像搜索结果流
- 只剩导航和页脚，没有正文
- 被跳到 `/user/profile/...`
- 标题、作者、正文都抓不到
- 明显风控页 / 登录页 / 空白页

### 建议的成功判定输出

```json
{
  "detail_status": "SUCCESS|FAILED|PARTIAL",
  "detail_failure_type": "DETAIL_ABORTED|DETAIL_REDIRECTED_TO_PROFILE|DETAIL_RENDER_EMPTY|DETAIL_RISK_OR_LOGIN|DETAIL_UNKNOWN_ERROR|",
  "success_signals": ["HAS_TITLE", "HAS_AUTHOR", "HAS_BODY", "HAS_COMMENTS"],
  "attempt_path": "WRAPPER|DETAIL|CLICK"
}
```

---

## 第六步：详情页正文提取

### 关键原则
**正文提取优先使用 `evaluate/DOM`，不要只依赖 snapshot。**

原因：
- snapshot 对小红书详情页有时抓不全
- 但 DOM 中常常已经存在完整标题、作者、正文、评论

### 推荐提取字段
对每条成功进入的详情页，提取：
- `url`
- `title`
- `author`
- `desc` / 正文摘要
- `body_text`
- `comment_count`（若能从文本中识别）
- `comment_samples`：前 3-5 条评论要点
- `engagement_signals`：点赞/收藏/评论等能抓到多少算多少

### 评论区使用原则
评论不是必须，但若存在真实讨论，价值很高：
- 可辅助判断是否广告
- 可反映真实用户反馈
- 对 AI 工具类话题尤其有价值

### 建议的结构化输出

```json
{
  "title": "...",
  "author": "...",
  "desc": "...",
  "body_text": "...",
  "comment_count": 30,
  "comment_samples": ["...", "...", "..."],
  "engagement_signals": {
    "likes": null,
    "collects": null,
    "comments": 30
  }
}
```

---

## 第七步：广告判断与评分

### 广告识别标准
符合任一项，可判为广告或低价值：
- 明显引流词：主页、私信、咨询、购买、加群、代做
- 文本模板化严重
- 品牌词堆砌但缺少具体使用场景
- 没有任何真实体验、对比、过程或问题描述
- 评论区明显灌水、缺少真实互动

### 价值内容标准
满足越多越好：
- 有真实使用场景
- 有具体体验和观点
- 有优缺点、踩坑点或替代方案讨论
- 评论区能补充更多信息
- 对用户关键词有直接帮助

### 输出字段
每条结果输出：
- `is_ad`：是 / 否 / 不确定
- `relevance_score`：0-10
- `value_score`：0-10
- `overall_score`：0-10
- `key_points`：1-3 条
- `reason`：保留或过滤理由
- `detail_status`：SUCCESS / FAILED / PARTIAL
- `detail_failure_type`：若失败则填写分类

### 建议的判定基线
- `relevance_score >= 8`：高度相关
- `value_score >= 7`：值得保留
- `overall_score <= 4`：通常可过滤

---

## 第八步：批量执行模板（新增）

这是将稳定器真正落成可执行流程的模板。

### 批量执行顺序

#### 批次 1：结果收集
- 进入搜索结果页
- 提取前 `8-12` 个候选
- 去重并结构化
- 先做首轮过滤

#### 批次 2：详情深挖
- 只挑 `3-5` 条候选进入详情页
- 优先高相关、结构完整、有作者名的结果
- 串行处理，不并行开多个详情页

#### 批次 3：补充样本
- 如果成功率低于 50%，不要立刻继续硬冲
- 先汇报失败类型分布，再决定是否补充尝试
- 若成功率正常，再补 2-3 条

### 单条详情的执行模板

1. 记录候选
2. 尝试包装链接
3. 验收详情成功信号
4. 若失败，尝试裸详情
5. 再验收
6. 若仍失败，根据需要尝试真实点击卡片
7. 成功则提取正文
8. 失败则分类记录

### 每条详情的最大尝试次数
建议：
- 包装链接：1 次
- 裸详情：1 次
- 真实点击：最多 1 次

即：
**单条结果最多 3 次尝试**，避免过度重复触发风控。

---

## 第九步：重试与节奏控制（新增）

### 重试原则
- 同一路径失败后，不要立即连续重试 3 次
- 失败后切换路径，而不是同路径硬刷
- 若连续 3 条结果都出现 `DETAIL_ABORTED`，暂停后续深挖，先汇报

### 节奏建议
- 每打开 1 条详情，至少间隔短暂停顿
- 避免高频快速打开多个详情页
- 如站点明显变慢、页面变空、验证码出现，立即停止

### 建议暂停条件
出现以下任一情况，应暂停深挖：
- 连续 3 条 `DETAIL_ABORTED`
- 连续 2 条跳到登录/风控
- DOM 结构明显失真
- 页面开始只返回导航/页脚模板

---

## 第十步：失败记录模板（新增）

失败不是无结果，而是调试资产。

### 建议记录结构

```json
{
  "note_id": "...",
  "author_name": "...",
  "attempts": [
    {"path": "WRAPPER", "result": "FAILED", "failure_type": "DETAIL_ABORTED"},
    {"path": "DETAIL", "result": "FAILED", "failure_type": "DETAIL_ABORTED"}
  ],
  "final_status": "FAILED",
  "remark": "包装与裸详情均被站点中断"
}
```

### 为什么要保留失败项
- 方便后续稳定性调优
- 能看出哪类作者/内容更容易失败
- 可同步到 Bitable 做长期观察

---

## 第十一步：汇总报告

建议格式：

```markdown
## 小红书搜索报告：<keyword>
搜索时间：YYYY-MM-DD HH:MM
结果卡片：Y
成功进入详情：X
失败详情：Z

### 值得看
1. <标题>
- 作者：@xxx
- 综合评分：8/10
- 关键观点：...
- 推荐理由：...
- 链接：...

### 已过滤
1. <标题或note_id>
- 原因：广告 / 低相关 / 详情进入失败 / 页面异常

### 进入失败记录
1. <note_id>
- 失败类型：DETAIL_ABORTED
- 备注：包装链接失败，裸详情也失败

## 综合结论
- 高频观点 1
- 高频观点 2
- 当前结果整体质量判断
- 后续建议（是否值得继续搜相近关键词）
```

---

## 第十二步：同步到 Feishu Bitable（可选）

推荐字段：
- 关键词
- 平台
- 标题
- 作者
- 是否广告
- 综合评分
- 相关度
- 详情状态
- 失败类型
- 核心观点
- 链接
- 搜索时间

### 建议
- 少量批次写入
- 把失败项也记录下来，方便后续调试稳定性
- 对成功和失败使用统一字段，便于统计成功率

---

## 执行中的进度汇报规范

长流程中按阶段汇报：
- 浏览器接入是否正常
- 是否进入搜索结果页
- 抽到了多少候选结果
- 详情进入成功/失败数量
- 失败类型分布
- 是否发现站点异常或风控
- 当前已经拿到多少可用正文样本
- 是否已完成报告或同步飞书

### 建议汇报节奏
- 每完成 1 个阶段汇报 1 次
- 不要每一条详情都单独刷屏
- 若出现连续失败或风控，立即汇报

---

## 错误处理

| 情况 | 处理方式 |
|---|---|
| `browser` 超时 | 先检查 gateway/browser 接入，不盲重试 |
| 未登录小红书 | 提示用户先登录 |
| 搜索结果页结构变化 | 改用 `evaluate` 重新识别链接类型 |
| 进入后跳到作者主页 | 标记 `DETAIL_REDIRECTED_TO_PROFILE`，回退 |
| `/explore/<id>` 打开中断 | 改走包装链接或真实点击卡片 |
| 包装链接打开中断 | 改走裸详情兜底 |
| 详情页只有页脚/导航 | 标记 `DETAIL_RENDER_EMPTY` |
| 验证码/风控 | 终止自动化，等待用户手动处理 |
| 页面脚本异常/资源异常 | 记录 console 错误，作为稳定性问题，不伪造成功 |

---

## 长期稳定性原则

1. **包装链接优先，裸详情兜底**
2. **详情成功必须验收，不看 URL 自嗨**
3. **正文提取优先用 DOM evaluate**
4. **失败要分类记录，不能混成“无结果”**
5. **接受部分成功，不追求假 100% 成功率**
6. **连续失败时暂停，优先保护账号和会话稳定性**

---

## 执行者备注

如果你是执行该 Skill 的智能体，请遵守：
- 不要为了凑数量而伪造详情分析
- 不要忽略失败分类
- 不要高频暴力打开详情页
- 一旦成功率明显下降，先汇报，再决定是否继续

---

## 关联 Skill

BOSS 直聘岗位搜索未来可复用同样的“详情进入稳定器”思路：
- 列表页结构化提取
- 多级详情进入路径
- 成功验收
- 失败分类
- 再做 AI 分析与汇总
