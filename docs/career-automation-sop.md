# Career Automation SOP / 操作手册

## 目标

把 OpenClaw 变成一套可持续运行的求职自动化系统，围绕以下主线工作：

1. 打开招聘站真实页面
2. 提取结果页岗位卡片
3. 进入详情页提取真实 JD
4. 保存为结构化文件
5. 进行岗位筛选与匹配分析
6. 仅对高价值岗位继续做简历与面试准备

当前默认主线：
- 主抓取：`miliger-playwright-scraper`
- 补充浏览器层：`playwright`
- 编排：`career-pipeline`
- 业务层：`job-intelligence` / `jd-fit-analyzer` / `resume-tailor` / `interview-prep-builder`

---

## 一、日常使用原则

### 1. 默认只打一条链，不同时摊开多个站
优先顺序：
1. 实习僧
2. 51job
3. 猎聘
4. 公司官网 / 校招页
5. BOSS（仅降级备用）

### 2. 不再走旧首页搜索框方案
禁止默认依赖：
- 首页搜索框输入
- 脆弱多点击链路
- 把 Crawl4AI 当主入口

### 3. 结果页和详情页优先
优先使用：
- 稳定搜索结果 URL
- 已打开的真实页面
- 详情页直链

### 4. 所有成功动作都要落文件
没有产物文件，就不算真正完成。

---

## 二、标准工作流

## Phase A：确定来源与搜索入口
输入：
- 关键词（如：C++ / 机器人 / 自动驾驶 / ROS）
- 城市（广州 / 深圳）
- 岗位类型（实习 / 校招 / 初级）

输出：
- 一个稳定结果页 URL
- 或一个已打开且可见的结果页标签

规则：
- 优先结果页，不优先首页
- 优先真实可见内容，不优先理论可抓内容

---

## Phase B：结果页抓取
目标：提取候选岗位卡片，落 `cards.json`

标准字段：
- `title`
- `company`
- `city`
- `salary`
- `schedule` / `experience_requirement`
- `education_requirement`（如可见）
- `tags`
- `summary`
- `detail_url`
- `extraction_confidence`

路径：
- `artifacts/jobs/<source>/<YYYY-MM-DD>/cards.json`

失败分类建议：
- `captcha-present`
- `result-page-empty`
- `selector-unstable`
- `detail-url-missing`

---

## Phase C：详情页抓取
目标：进入详情页，提取真实 JD 主体

标准产物：
- `details/<job-id>.json`
- `details/<job-id>.md`

JSON 字段建议：
- `title`
- `company`
- `city`
- `salary`
- `education_requirement`
- `experience_requirement`
- `conversion_opportunity`
- `tags`
- `responsibilities[]`
- `requirements[]`
- `application_requirements`
- `work_location`
- `company_profile`
- `extraction_confidence`
- `failures[]`

规则：
- 优先提取页面主体真实文字
- 如果验证码存在但主体可见，允许继续提取，同时记录 `captcha-present`
- 不要假装详情页成功，如果只拿到了标题/卡片摘要

---

## Phase D：岗位过滤
由 `job-intelligence` 执行。

保留优先：
- 广州 / 深圳
- C++ / Linux / ROS / OpenCV / 系统工程 / 分布式 / 机器人 / 自动驾驶
- 实习 / 校招 / 初级工程岗

下调或淘汰：
- 培训 / 外包 / 伪技术岗
- 偏销售支持岗
- 与主线完全偏离的行业岗位

输出：
- kept roles
- rejected roles
- failure statistics
- recommended next actions

---

## Phase E：匹配分析
由 `jd-fit-analyzer` 执行。

输入：
- 真实 JD JSON / MD
- `skills/references/user-career-profile.md`
- `skills/references/resume-master.md`

输出必须包含：
1. overall verdict
2. strong matches
3. partial matches / adjacent evidence
4. clear gaps
5. packaging opportunities
6. risk notes
7. application recommendation
8. resume adjustment hints
9. confidence note

规则：
- 不编造实习经历
- 不把竞赛包装成企业经验
- 但要真实翻译为工程证据

---

## Phase F：只对高价值岗位做下游动作
### 强目标
- 简历调整
- 面试准备

### 可投目标
- 先做简历建议

### 低价值/偏离目标
- 只保留 fit 分析，不继续深挖

---

## 三、推荐目录结构

```text
artifacts/
  jobs/
    <source>/
      <YYYY-MM-DD>/
        cards.json
        summary.md
        fit-analysis-batch-1.md
        details/
          <job-id>.json
          <job-id>.md
```

---

## 四、失败与人工介入规则

### 遇到以下情况必须人工介入
1. 登录
2. 滑块验证码主体不可见
3. 投递动作
4. 外发消息 / 简历投递 / 公开操作

### 遇到以下情况允许继续自动跑
1. 页面有验证码 iframe，但主体 JD 仍可见
2. 页面可见、链接可见，但交互略不稳定
3. 结果页可读但部分字段不完整

### 停止重试规则
- 同一脆弱动作失败 3 次就停止
- 不要无限循环点击同一页面元素

---

## 五、当前已验证成功的样例

来源：`实习僧`
关键词：`c++`
城市：`广州`

已成功产物：
- `artifacts/jobs/shixiseng/2026-04-02/cards.json`
- `artifacts/jobs/shixiseng/2026-04-02/details/inn_c7ueadyyw59b.json`
- `artifacts/jobs/shixiseng/2026-04-02/details/inn_3xvqodufcddt.json`
- `artifacts/jobs/shixiseng/2026-04-02/details/inn_cll7eaz645sb.json`
- `artifacts/jobs/shixiseng/2026-04-02/fit-analysis-batch-1.md`

说明：
- 页面存在腾讯滑块 iframe
- 但主体 JD 内容仍可见并成功提取
- 这证明 Playwright-first 主线可以工作

---

## 六、后续迭代顺序

### 第 1 优先级
扩展同一站点更多样本，稳定字段与失败分类

### 第 2 优先级
迁移到 51job / 猎聘等第二来源

### 第 3 优先级
把高优先岗位自动串到简历调整与面试准备

### 第 4 优先级
再考虑真正的批量化与调度

---

## 七、一句话定义

这套系统的正确定义不是“网页搜索工具”，而是：

**以 Playwright-first 浏览器提取为入口，围绕真实 JD 获取、岗位筛选、匹配分析和后续求职准备构建的自动化工作流。**
