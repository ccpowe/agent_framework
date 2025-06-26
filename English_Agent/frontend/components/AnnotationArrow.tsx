// components/AnnotationArrow.tsx
'use client';

import React from 'react';

interface AnnotationArrowProps {
  fromRef: React.RefObject<HTMLElement>; // 指向错误元素的引用
  toRef: React.RefObject<HTMLElement>;   // 指向修正建议元素的引用
  containerRef: React.RefObject<HTMLElement>; // 包含这两个元素的最近的定位父容器的引用
  color?: string; // 箭头颜色
  strokeWidth?: number; // 箭头线条宽度
  visible: boolean; // 控制箭头是否可见，用于动画
}

const AnnotationArrow: React.FC<AnnotationArrowProps> = ({
  fromRef,
  toRef,
  containerRef,
  color = 'red', // 默认红色
  strokeWidth = 2,
  visible,
}) => {
  const [pathData, setPathData] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (fromRef.current && toRef.current && containerRef.current && visible) {
      const fromRect = fromRef.current.getBoundingClientRect();
      const toRect = toRef.current.getBoundingClientRect();
      const containerRect = containerRef.current.getBoundingClientRect();

      // 计算相对于父容器的坐标
      const fromX = fromRect.left - containerRect.left + fromRect.width / 2;
      const fromY = fromRect.top - containerRect.top + fromRect.height / 2;
      
      // 目标元素的中心点，或者根据需要调整到边框
      const toX = toRect.left - containerRect.left + toRect.width / 2;
      // 让箭头指向修正框的底部中间，这样箭头尖端在文字下方
      const toY = toRect.top - containerRect.top + toRect.height; 


      // 简单的直线箭头路径
      // M = moveto, L = lineto
      // 考虑一个简单的曲线或折线，以避免直接穿过文本
      // 例如，从 from 的底部中心，向上一点，然后水平，再向下到 to 的顶部中心

      let d = `M ${fromX} ${fromRect.bottom - containerRect.top}`; // 从错误元素的底部中心开始
      
      // 控制点，用于创建简单的弧线或折线，避免直接穿过元素
      // 这里我们让箭头先稍微向下，然后水平移动，再向上/下指向目标
      const controlY1 = fromRect.bottom - containerRect.top + 10; // 向下一点
      const controlX = fromX + (toX - fromX) / 2; // 水平中点
      const controlY2 = toRect.top - containerRect.top - 10; // 目标上方一点

      // 使用二次贝塞尔曲线 Q controlX,controlY targetX,targetY
      // 或者三次贝塞尔曲线 C c1X,c1Y c2X,c2Y targetX,targetY
      // 这里用一个简单的折线示例：
      // 从 fromRect 底部出发
      const startX = fromRect.left - containerRect.left + fromRect.width / 2;
      const startY = fromRect.bottom - containerRect.top;

      // 修正框的顶部中心
      const endX = toRect.left - containerRect.left + toRect.width / 2;
      const endY = toRect.top - containerRect.top;
      
      // 简单的折线：向下 -> 水平 -> 向上/下
      const midY = Math.max(startY, endY) + 20; // 在两者下方20px处折弯

      if (Math.abs(startX - endX) < 30) { // 如果水平距离很近，直接画直线或微弯的线
         d = `M ${startX} ${startY} Q ${startX} ${startY + (endY - startY)/2} ${endX} ${endY}`;
      } else if (endY < startY) { // 修正框在错误元素的上方
        const intermediateY = endY - 15; // 目标上方15px
        d = `M ${startX} ${startY} L ${startX} ${startY + 10} L ${endX} ${intermediateY + 10} L ${endX} ${endY}`;
      } else { // 修正框在错误元素的下方或同一水平线
        const intermediateY = startY + 15; // 起点下方15px
         d = `M ${startX} ${startY} L ${startX} ${intermediateY} L ${endX} ${intermediateY} L ${endX} ${endY}`;
      }

      setPathData(d);
    } else {
      setPathData(null);
    }
  }, [fromRef, toRef, containerRef, visible, fromRef.current, toRef.current, containerRef.current]); // 依赖项确保在元素加载后计算

  if (!pathData || !visible) {
    return null;
  }

  return (
    <svg
      className="absolute top-0 left-0 w-full h-full pointer-events-none"
      style={{ zIndex: 5 }} // 确保箭头在其他内容之上，但在tooltip之下
    >
      <defs>
        <marker
          id={`arrowhead-${color.replace('#', '')}`}
          markerWidth="10"
          markerHeight="7"
          refX="0" // 对于路径末端的箭头，refX 通常是 markerWidth 或路径末端点
          refY="3.5"
          orient="auto"
          markerUnits="strokeWidth"
        >
          <polygon points="0 0, 10 3.5, 0 7" fill={color} />
        </marker>
      </defs>
      <path
        d={pathData}
        stroke={color}
        strokeWidth={strokeWidth}
        fill="none"
        markerEnd={`url(#arrowhead-${color.replace('#', '')})`}
        style={{
          transition: 'opacity 0.3s ease-in-out, stroke-dashoffset 0.5s ease-in-out',
          opacity: visible ? 1 : 0,
        }}
      />
    </svg>
  );
};

export default AnnotationArrow;
