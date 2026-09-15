#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Mechanism Diagram Generator (SVG)
Generates peer-reviewed academic mechanism diagrams in pure SVG vector format.
Strictly Pure White Background & Black Text, Centered, No Titles, No Annotations.
Adheres to CSSCI/SSCI Publishing Standard:
- HeiTi large font (font-weight="normal") for primary concepts
- Bold FangSong (font-weight="bold") for secondary descriptors and link labels
- Pure black/white vector aesthetics with zero marker-start
"""

import sys
import os
import argparse

FONT_HEITI = "'SimHei', 'Heiti SC', 'Microsoft YaHei', sans-serif"
FONT_FANGSONG = "'FangSong', 'STFangsong', 'FangSong_GB2312', 'SimSun', serif"

def get_defs():
    return """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#000000"/>
    </marker>
  </defs>"""

def create_pipeline_svg(stages=None):
    if not stages:
        stages = ["情境输入", "动因激发", "行动机制", "效能产出"]
    w, h = 960, 640
    box_w, box_h = 170, 120
    total_boxes = len(stages)
    total_w = 820
    start_x = (w - total_w) / 2
    y = 230
    gap = (total_w - total_boxes * box_w) / (total_boxes - 1)
    
    boxes = ""
    for i, s in enumerate(stages):
        bx = start_x + i * (box_w + gap)
        boxes += f"""
        <!-- Stage {i+1} -->
        <g transform="translate({bx}, {y})">
          <rect width="{box_w}" height="{box_h}" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
          <rect width="{box_w}" height="38" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
          <text x="{box_w/2}" y="25" font-family="{FONT_FANGSONG}" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">阶段 {i+1}</text>
          <text x="{box_w/2}" y="82" font-family="{FONT_HEITI}" font-size="20" font-weight="normal" fill="#000000" text-anchor="middle">{s}</text>
        </g>
        """
        if i < total_boxes - 1:
            ax1 = bx + box_w
            ax2 = ax1 + gap
            boxes += f"""
            <line x1="{ax1+8}" y1="{y+box_h/2}" x2="{ax2-8}" y2="{y+box_h/2}" stroke="#000000" stroke-width="2" marker-end="url(#arrow)" />
            <text x="{(ax1+ax2)/2}" y="{y+box_h/2-12}" font-family="{FONT_FANGSONG}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">传导驱动</text>
            """
    
    # Feedback loop
    fb_x1 = start_x + (total_boxes-1)*(box_w+gap) + box_w/2
    fb_x2 = start_x + box_w/2
    boxes += f"""
    <!-- Long Feedback Loop -->
    <path d="M {fb_x1} {y+box_h} L {fb_x1} {y+box_h+85} L {fb_x2} {y+box_h+85} L {fb_x2} {y+box_h+16}" fill="none" stroke="#000000" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#arrow)" />
    <text x="{(fb_x1+fb_x2)/2}" y="{y+box_h+74}" font-family="{FONT_FANGSONG}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">动态自适应演进与再生产反馈回路</text>
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
{get_defs()}
  <rect width="{w}" height="{h}" fill="#ffffff" />
  <rect x="40" y="40" width="{w-80}" height="{h-80}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  {boxes}
</svg>"""
    return svg

def create_hierarchy_svg():
    w, h = 900, 700
    levels = [
        ("宏观制度层", "国家战略导向 · 法律规范供给 · 治理体制激励"),
        ("中观组织层", "地方政府协同 · 资源要素整合 · 平台运营中枢"),
        ("微观行动层", "多元主体响应 · 基层实践创新 · 动态效能释放"),
    ]
    svg_body = ""
    y_start = 100
    box_w = 740
    box_h = 130
    x = (w - box_w) / 2
    gap = 60

    for i, (lvl_title, lvl_desc) in enumerate(levels):
        cy = y_start + i * (box_h + gap)
        svg_body += f"""
        <g transform="translate({x}, {cy})">
          <rect width="{box_w}" height="{box_h}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
          <rect x="18" y="16" width="130" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
          <text x="83" y="39" font-family="{FONT_FANGSONG}" font-size="15" font-weight="bold" fill="#000000" text-anchor="middle">{lvl_title}</text>
          <text x="180" y="40" font-family="{FONT_HEITI}" font-size="20" font-weight="normal" fill="#000000">{lvl_desc.split(' · ')[0]}</text>
          <line x1="18" y1="64" x2="{box_w-18}" y2="64" stroke="#000000" stroke-width="1" stroke-dasharray="4 4" />
          <text x="35" y="98" font-family="{FONT_FANGSONG}" font-size="15" font-weight="bold" fill="#000000">关键要素：{lvl_desc}</text>
        </g>
        """
        if i < len(levels) - 1:
            arrow_y1 = cy + box_h + 4
            arrow_y2 = cy + box_h + gap - 4
            mid_y = (arrow_y1 + arrow_y2) / 2
            # Left downward arrow
            svg_body += f"""
            <line x1="{x+180}" y1="{arrow_y1}" x2="{x+180}" y2="{arrow_y2}" stroke="#000000" stroke-width="1.8" marker-end="url(#arrow)" />
            <text x="{x+170}" y="{mid_y+4}" font-family="{FONT_FANGSONG}" font-size="13" font-weight="bold" fill="#000000" text-anchor="end">赋能传导</text>
            <!-- Right upward feedback arrow -->
            <line x1="{x+box_w-180}" y1="{arrow_y2}" x2="{x+box_w-180}" y2="{arrow_y1}" stroke="#000000" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arrow)" />
            <text x="{x+box_w-170}" y="{mid_y+4}" font-family="{FONT_FANGSONG}" font-size="13" font-weight="bold" fill="#000000" text-anchor="start">实践反馈</text>
            """

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
{get_defs()}
  <rect width="{w}" height="{h}" fill="#ffffff" />
  <rect x="40" y="40" width="{w-80}" height="{h-80}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  {svg_body}
</svg>"""

def create_dual_svg():
    w, h = 960, 640
    # Left system and right system
    sys_w, sys_h = 360, 440
    y = 100
    x_left = 70
    x_right = w - 70 - sys_w

    svg_body = f"""
    <!-- Left Subsystem -->
    <g transform="translate({x_left}, {y})">
      <rect width="{sys_w}" height="{sys_h}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="{sys_w/2}" y="42" font-family="{FONT_HEITI}" font-size="22" font-weight="normal" fill="#000000" text-anchor="middle">制度驱动系统</text>
      <line x1="25" y1="62" x2="{sys_w-25}" y2="62" stroke="#000000" stroke-width="1.2" />
      <rect x="35" y="90" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="132" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">行政规制与激励供给</text>
      <rect x="35" y="190" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="232" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">组织协调与资源再分配</text>
      <rect x="35" y="290" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="332" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">合规审查与监督考评</text>
    </g>

    <!-- Right Subsystem -->
    <g transform="translate({x_right}, {y})">
      <rect width="{sys_w}" height="{sys_h}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
      <text x="{sys_w/2}" y="42" font-family="{FONT_HEITI}" font-size="22" font-weight="normal" fill="#000000" text-anchor="middle">市场实践系统</text>
      <line x1="25" y1="62" x2="{sys_w-25}" y2="62" stroke="#000000" stroke-width="1.2" />
      <rect x="35" y="90" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="132" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">多元主体利益博弈</text>
      <rect x="35" y="190" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="232" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">契约安排与交易治理</text>
      <rect x="35" y="290" width="{sys_w-70}" height="70" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.4" />
      <text x="{sys_w/2}" y="332" font-family="{FONT_FANGSONG}" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">微观效能与创新释放</text>
    </g>

    <!-- Interactive Corridor in Center -->
    <line x1="{x_left+sys_w+10}" y1="225" x2="{x_right-10}" y2="225" stroke="#000000" stroke-width="1.8" marker-end="url(#arrow)" />
    <text x="{w/2}" y="215" font-family="{FONT_FANGSONG}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">制度授权与资源注入</text>

    <line x1="{x_right-10}" y1="325" x2="{x_left+10+sys_w}" y2="325" stroke="#000000" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#arrow)" />
    <text x="{w/2}" y="315" font-family="{FONT_FANGSONG}" font-size="14" font-weight="bold" fill="#000000" text-anchor="middle">效能回报与诉求表达</text>
    """

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
{get_defs()}
  <rect width="{w}" height="{h}" fill="#ffffff" />
  <rect x="35" y="35" width="{w-70}" height="{h-70}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  {svg_body}
</svg>"""

def main():
    parser = argparse.ArgumentParser(description="Academic SVG Mechanism Diagram Generator")
    parser.add_argument("--type", default="pipeline", choices=["pipeline", "hierarchy", "dual"], help="Diagram archetype")
    parser.add_argument("--output", default="mechanism_diagram.svg", help="Output SVG path")
    args = parser.parse_args()

    if args.type == "pipeline":
        svg_content = create_pipeline_svg()
    elif args.type == "hierarchy":
        svg_content = create_hierarchy_svg()
    elif args.type == "dual":
        svg_content = create_dual_svg()
    else:
        svg_content = create_pipeline_svg()

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated SVG ({args.type}): {args.output}")

if __name__ == "__main__":
    main()
