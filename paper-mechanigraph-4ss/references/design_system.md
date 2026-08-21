# 学术机制图 SVG 矢量设计系统指南 (Academic Mechanism SVG Design System)

本规范为顶级学术期刊 (CSSCI / SSCI) 机制图矢量 SVG 绘制的底层设计系统。所有 Agent 与自动化生成脚本必须严格遵守以下规范。

---

## 1. 核心制图红线 (Hard Rules)

1. **绝对禁止包含图表标题**：图表标题（如“图1 XXX机制模型”）应由论文作者在正文排版中手写插入，矢量图内绝不能包含任何主标题。
2. **绝对禁止包含作者或来源注释**：图表底部不得包含“作者自制”、“数据来源：XXX”等任何辅助性注释。
3. **严格纯粹白底黑字规范 (Pure White Background & Black Text)**：
   - **绝对禁止任何深色底块、灰色底块填充**（严禁 `#333333`, `#f5f5f5`, `#eeeeee` 等任何灰度填充）；
   - **所有卡片与形状容器统一使用纯白填充** `fill="#ffffff"` 或透明 `fill="none"`；
   - **所有文字统一使用纯黑色** `fill="#000000"`（严禁白字反白）；
   - **所有线条与边框统一使用纯黑** `stroke="#000000"`。
4. **动态自适应固定画布与物理视口绑定 (Dynamic Fixed Viewport)**：
   * **动态尺寸计算法则**：根据图表内容的信息密度和流动方向动态决定 `W` (宽) 与 `H` (高)：
     * **标准中等密度机制图**：`W = 900, H = 600`
     * **多阶段长横向因果链 (5~7阶段)**：`W = 1200 ~ 1400, H = 650 ~ 750`
     * **深层纵向卡片体系 (4~6层级)**：`W = 900 ~ 1000, H = 1000 ~ 1200`
     * **对称环形/正多边形网络**：`W = 800 ~ 900, H = 800 ~ 900`
   * **视口与物理像素严格 1:1 声明公式**：
     `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">`
   * **严禁使用 `width="100%"`**，确保生成的 SVG 在任何设备与渲染器中均能按所计算的 `(W, H)` 比例实现像素级绝对对称居中！
   * 外大边框公式：`<rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="8" fill="none" stroke="#000000" stroke-width="1.8" />`。
   - **严禁局部割裂式调参**：在 900x600 画布中必须遵循**三层互不侵犯高度带 (Non-Overlapping Spatial Bands)**：
     * **顶部宏观趋势带 (`y: 40 ~ 150`)**：容纳全局 S 曲线、趋势标签、Y 轴顶端标题，严禁任何实体卡片侵入；
     * **中部实体交互带 (`y: 160 ~ 470`)**：容纳所有阶梯/层级卡片及正交连线，顶层卡片上限为 `y=170`；
     * **底部基线带 (`y: 480 ~ 560`)**：容纳 X 轴、原点、右下轴标签与安全留白；
   - 调整任一元素必须执行**全局联动 (Holistic Cascading)**，确保所有上下、左右间距同时满足安全标准！
5. **曲线轨迹与文本/卡片零重叠 (Zero-Collision Curve Clearance)**：
   - 贝塞尔曲线（尤其是跨越卡片的 S 曲线）具有曲率下凹特性，**严禁使用卡片中心或边缘顶点作为曲线锚点**。
   - 全局趋势曲线必须在 Y 轴上至少抬高 `30px ~ 50px`（即安全净空），使其完整悬浮于所有实体上方。
   - 卡片之间的因果跃迁统一采用阶梯正交折线 (`M x1 y1 L x2 y1 L x2 y2 L x3 y2`) 精确对接边缘。

---

## 2. 画布与视口规范 (Canvas & Viewport)

* **标准视口**：`viewBox="0 0 900 600"`（4:3 / 3:2 黄金比例机制图标准）或 `viewBox="0 0 1000 600"`（宽屏通栏图）。
* **安全外边距**：四周统一保留 `padding = 40px ~ 60px` 呼吸留白。
* **栅格对齐**：所有矩形节点中心与连接线锚点优先对齐至 5px 或 10px 的整数倍坐标。

---

## 3. 学术排版与字号阶梯 (Typography & Font Stacks)

* **字体栈与排版规范**：
  * **主模块/核心概念（强调项）**：全面采用**标准黑体 (HeiTi)**，**不强制加粗 (`font-weight="normal"`)**，仅通过**放大字号（`20px ~ 24px`）**体现层级，保持版面清秀疏朗；
    * 字体栈：`'SimHei', 'Heiti SC', 'Microsoft YaHei', sans-serif`；
  * **次级节点、细分指标、连线动词、括号说明（非强调项）**：全面采用**加粗仿宋体 (`font-weight="bold"`)**，消除仿宋原字体偏细导致印刷不清晰的弊端；
    * 字体栈：`'FangSong', 'STFangsong', 'FangSong_GB2312', 'SimSun', serif`，字号 `14px ~ 16px`；
  * **英文/数字**：`'Times New Roman', 'Arial', sans-serif`。

---

## 4. 外围大边框样式选项 (Outer Frame Styles)
1. **实线大外框 (Solid Frame)**：`<rect x="40" y="40" width="820" height="520" rx="8" fill="none" stroke="#000000" stroke-width="1.8" />`（经典正式出版风）；
2. **虚线大外框 (Dashed Frame)**：`<rect x="40" y="40" width="820" height="520" rx="8" fill="none" stroke="#000000" stroke-width="1.8" stroke-dasharray="8 6" />`（开放宏观制度/外部环境风）；
3. **无边框开放画布 (Frameless / Canvas)**：不绘制最外层 `<rect>`，机制图直接在纯白画布中居中舒展（现代极简风）。

---

## 4. 文字与图形元素黄金间距规范 (Text-to-Element Spacing)

文字与图形元素之间的物理距离必须严格控制在“黄金呼吸区间”内，严禁过近（拥挤窒息/重叠风险）或过远（割裂脱节/归属不明）：

### (1) 卡片内文字与边框的内边距 (Internal Padding)
* **黄金间距**：`12px ~ 20px`。
* **规则**：
  * 文字基线与卡片顶部边框：第一行文字中心距卡片顶边 `35px ~ 40px`；
  * 文字左右两端与卡片左右边框：保留至少 `15px` 安全防撞边距；
  * **严禁贴边（< 8px）** 或 **空旷涣散（> 30px 且卡片内部大片死白）**。

### (2) 连线标注文字与箭头/线条的间距 (Label-to-Line Clearance)
* **黄金间距**：`8px ~ 12px` (水平线) / `25px ~ 40px` (斜线与陡峭曲线)。
* **规则**：
  * 水平连线文字位于线条正上方 `8px ~ 10px`（即 `y = line_y - 8`）；
  * 垂直连线文字位于线条左侧或右侧 `10px ~ 14px`；
  * **斜线与曲线上方文本净空红线**：由于曲线/斜线具有倾斜角，水平文字串放置其上方时，两端极易蹭线。**必须按文字包围盒离曲线最近的拐角计算，确保整段文字的任意像素点与曲线距离均保持在 `25px ~ 40px` 的充裕净空高度**，严禁末端贴近或粘连！
  * **严禁文字直接骑跨压在连接线上**，亦**严禁离连线 > 20px**（水平简单线）。
6. **连线侧边标注显式对齐铁律 (Explicit Text-Anchor for Parallel Flows)**：
   - 竖直/倾斜平行双向指示线两侧标注：
     * **左侧文本**：强制使用 `text-anchor="end"`，并预留 `12px ~ 15px` 间距；
     * **右侧文本**：强制使用 `text-anchor="start"`，并预留 `12px ~ 15px` 间距；
     * **严禁盲目使用 `text-anchor="middle"`** 导致 4 字以上中文字宽穿透压线！
7. **跨层纵向实体呼吸间距 (Inter-Tier Vertical Clearance $\ge 70\text{px}$)**：
   - 上下相邻卡片之间若有双向交互连线与文本，物理净距必须 $\ge 70\text{px}$，箭头端点距离边框预留 $6\sim 8\text{px}$。
8. **跨系统长连接线与分箱边界走廊 (Cross-System Link Corridor)**：
   - 跨系统连接线必须从源卡片完整延伸至目标容器边界；
   - 标注文本必须位于两系统空旷正中，离任何分箱边框保持 $\ge 35\text{px}$ 净空，严禁被虚线横切。
9. **箭头起点零三角铁律与双向交互双线规范 (Zero Marker-Start Rule)**：
   - 所有单向连线**仅在终点声明 `marker-end="url(#arrow)"`**，**严禁在起点添加 `marker-start`**；
   - 箭头的起点必须是平直光滑的端点，严禁倒刺小三角撞击发射端框体；
   - 实体间的双向互动**一律采用两条平行的独立单向箭头线**（一条 A 指向 B，一条 B 指向 A），实现清爽专业的学术出版质感。
10. **左右双系统/复合架构全域配平法则 (Dual-System Horizontal Balancing)**：
   - 复合架构中，左侧总宽度 + 中间走廊 + 右侧总宽度必须精确匹配画布可用宽度；
   - 左系统最左侧与右系统最右侧距离外边框必须严格相等（$\approx 40\text{px}$）；
   - 左右两子系统内部的主轴必须分别居中对齐，消除局部偏向或重心倾斜。
11. **文本包围盒与容器边界安全验算 (Text Bounding-box vs Container Width)**：
   - 设文本包含 $N$ 个中文字符，字号为 $S\text{px}$，文本物理宽度约为 $W_{\text{text}} \approx N \times S$；
   - 必须强制满足 $W_{\text{text}} + 2 \times \text{Padding}_{\text{safe}} \le W_{\text{container}}$（其中 $\text{Padding}_{\text{safe}} \ge 25\text{px}$）；
   - 长标题（$\ge 30$ 字）字号强制降至 `13.5px ~ 14px` 或分行排版，彻底消除横切卡片与穿透分箱现象。
12. **XML 注释与转义规约 (XML Syntax & Escaping Guardrails)**：
   - 严禁在 SVG 注释中包含 `--`（如 `<!-- --- Card 1 --- -->`），一律使用 `<!-- === Card 1 === -->`；
   - 生成脚本必须使用 Unicode 字符（如 `→`, `·`, `〔 〕`）或对反斜杠严格转义，杜绝 `$ ightarrow$` 等乱码事故。
13. **跨层级/跨系统连线零穿透铁律 (Cross-Container Boundary & Badge Zero-Penetration)**：
   - **严禁连线贯穿标题徽标**：当目标容器顶部设有居中/偏置标题徽章/药丸标签 (`[X_min, X_max] × [Y_min, Y_max]`) 时，从上方引出的所有垂直/倾斜连接线绝对禁止横切该徽章及文字；
   - **精准外缘停靠**：系统级宏观映射箭头终点必须精准停靠在目标容器外边框顶部外缘（`Y_end = Y_container_top - 2px`）或徽标外侧走廊，严禁连线直接刺入容器内部；
   - **避让折线流向**：若需连接容器内特定子卡片，连线必须走标题徽章两侧走廊（`X < X_badge_min - 20px` 或 `X > X_badge_max + 20px`）或采用正交折线避让，杜绝中轴直线硬穿。

### (3) 多行文字行间距 (Line Height & Spacing)
* **主标题与副标题/指标文字**：垂直间距保持在 `24px ~ 28px`（如主标题 `y=40`，副标题 `y=68`）。
* **多行指标列表**：行间距保持在 `20px ~ 24px`。

### (4) 外部文字与相邻图形间距 (External Separation)
* 轴标签、外部注释性说明与卡片外框必须保持 `15px ~ 25px` 的明确独立间距。

---

## 5. 元素与元素实体间黄金间隙规范 (Inter-Element Clearance & Gap)

机制图中所有并列、相邻或互动的独立几何图形（卡片、圆形、圆环、齿轮、分区分箱）之间**必须保留恰当的物理空隙 (Breathing Gap)**，严禁硬性相切、紧贴或挤压：

### (1) 同层级并列卡片/节点间距 (Sibling Element Gap)
* **黄金间距**：`25px ~ 45px`。
* **规则**：
  * 水平并列的卡片之间（如 Pipeline 阶段卡片）间距统一保持在 `30px ~ 45px`；
  * 垂直并列的层级卡片之间间距保持在 `25px ~ 35px`；
  * **严禁贴合（< 15px 显得拥挤粘连）** 或 **疏离（> 60px 导致视觉流动性断裂）**。

### (2) 环形/多主体与中枢中介节点的间距 (Orbit-to-Center Clearance)
* **黄金间距**：`20px ~ 35px`。
* **规则**：
  * 圆形轨道、齿轮虚线环与中间连接矩形卡片之间**绝对严禁直接贴边相切**；
  * 必须在两者之间预留 `20px ~ 30px` 的清晰空隙，并通过明确的连接箭头（`<line>` 或 `<path>`）进行跨越桥接。

### (3) 分区分箱内子元素与外层分箱边框的留白 (Container Margin)
* **黄金间距**：`20px ~ 30px`。
* **规则**：
  * 大分箱外框（如宏观/中观/微观容器）与其内部容纳的小子卡片之间，四周必须留出至少 `20px` 的均匀衬垫空隙。

---

## 4. 标准元素组件库 (Component Library)

### (1) `<defs>` 标记与箭头库
```xml
<defs>
  <!-- 实心黑箭头 (主干传导) -->
  <marker id="arrow-solid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#000000" />
  </marker>

  <!-- 虚线中灰箭头 (反馈/辅助传导) -->
  <marker id="arrow-gray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#666666" />
  </marker>

  <!-- 空心粗箭头 (阶段跃迁) -->
  <marker id="arrow-hollow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#ffffff" stroke="#000000" stroke-width="1.5" />
  </marker>
</defs>
```

### (2) 容器与卡片样式
* **主外框/宏观边界**：
  `<rect x="40" y="40" width="820" height="520" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />`
* **虚线分区分箱**：
  `<rect x="60" y="70" width="240" height="460" rx="6" fill="#fafafa" stroke="#666666" stroke-width="1.2" stroke-dasharray="6 4" />`
* **标准实体卡片**：
  `<rect x="80" y="100" width="200" height="70" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5" />`
* **核心强调高亮卡片 (反白)**：
  `<rect x="350" y="250" width="200" height="80" rx="6" fill="#333333" stroke="#000000" stroke-width="1.5" />`
  `<text x="450" y="295" font-family="'Microsoft YaHei', sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">核心机制中枢</text>`

### (3) 连接线与语义路径
* **直接因果线**：`<line x1="100" y1="200" x2="250" y2="200" stroke="#000000" stroke-width="1.8" marker-end="url(#arrow-solid)" />`
* **正交直角折线**：`<path d="M 300 200 L 400 200 L 400 350 L 500 350" fill="none" stroke="#000000" stroke-width="1.8" marker-end="url(#arrow-solid)" />`
* **长跨度反馈回路**：`<path d="M 800 450 L 800 520 L 100 520 L 100 450" fill="none" stroke="#666666" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#arrow-gray)" />`
* **弧形关系连线**：`<path d="M 200 150 Q 300 80 400 150" fill="none" stroke="#000000" stroke-width="1.5" marker-end="url(#arrow-solid)" />`
