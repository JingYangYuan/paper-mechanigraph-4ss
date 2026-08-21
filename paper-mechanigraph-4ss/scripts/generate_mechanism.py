#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Academic Mechanism Diagram Generator (SVG)
Generates peer-reviewed academic mechanism diagrams in pure SVG vector format.
Strictly Pure White Background & Black Text, Centered, No Titles, No Annotations.
"""

import sys
import os
import argparse

def get_defs():
    return """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#000000"/>
    </marker>
  </defs>"""

def create_pipeline_svg(stages=None):
    if not stages:
        stages = ["情境输入", "动因激发", "行动机制", "效能产出"]
    w, h = 900, 600
    box_w, box_h = 160, 110
    total_boxes = len(stages)
    total_w = 760
    start_x = (w - total_w) / 2
    y = 220
    gap = (total_w - total_boxes * box_w) / (total_boxes - 1)
    
    boxes = ""
    for i, s in enumerate(stages):
        bx = start_x + i * (box_w + gap)
        boxes += f"""
        <!-- Stage {i+1} -->
        <g transform="translate({bx}, {y})">
          <rect width="{box_w}" height="{box_h}" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
          <rect width="{box_w}" height="36" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
          <text x="{box_w/2}" y="24" font-family="'Microsoft YaHei', sans-serif" font-size="16" font-weight="bold" fill="#000000" text-anchor="middle">阶段 {i+1}</text>
          <text x="{box_w/2}" y="76" font-family="'Microsoft YaHei', sans-serif" font-size="18" font-weight="bold" fill="#000000" text-anchor="middle">{s}</text>
        </g>
        """
        if i < total_boxes - 1:
            ax1 = bx + box_w
            ax2 = ax1 + gap
            boxes += f"""
            <line x1="{ax1+5}" y1="{y+box_h/2}" x2="{ax2-5}" y2="{y+box_h/2}" stroke="#000000" stroke-width="2" marker-end="url(#arrow)" />
            <text x="{(ax1+ax2)/2}" y="{y+box_h/2-10}" font-family="'Microsoft YaHei', sans-serif" font-size="14" fill="#000000" text-anchor="middle">传导驱动</text>
            """
    
    # Feedback loop
    fb_x1 = start_x + (total_boxes-1)*(box_w+gap) + box_w/2
    fb_x2 = start_x + box_w/2
    boxes += f"""
    <!-- Long Feedback Loop -->
    <path d="M {fb_x1} {y+box_h} L {fb_x1} {y+box_h+80} L {fb_x2} {y+box_h+80} L {fb_x2} {y+box_h+15}" fill="none" stroke="#000000" stroke-width="1.8" stroke-dasharray="6 4" marker-end="url(#arrow)" />
    <text x="{(fb_x1+fb_x2)/2}" y="{y+box_h+70}" font-family="'Microsoft YaHei', sans-serif" font-size="15" fill="#000000" text-anchor="middle">动态自适应演进与再生产反馈回路</text>
    """

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
{get_defs()}
  <rect width="{w}" height="{h}" fill="#ffffff" />
  <rect x="40" y="40" width="{w-80}" height="{h-80}" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.8" />
  {boxes}
</svg>"""
    return svg

def main():
    parser = argparse.ArgumentParser(description="Academic SVG Mechanism Diagram Generator")
    parser.add_argument("--type", default="pipeline", choices=["pipeline", "hierarchy", "network", "loop", "steps", "gear"], help="Diagram archetype")
    parser.add_argument("--output", default="mechanism_diagram.svg", help="Output SVG path")
    args = parser.parse_args()

    svg_content = create_pipeline_svg()
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated SVG: {args.output}")

if __name__ == "__main__":
    main()
