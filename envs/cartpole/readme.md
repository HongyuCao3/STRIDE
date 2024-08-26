# CartPole Demo

本部分参考其他envs实现

## 问题定义

1. 变量

   1. cart_position：-2.4 ~ 2.4
   2. cart_speed：-inf ~ inf
   3. pole_angle：-0.5 ～ 0.5 （radian）
   4. pole_angular_velocity：-inf ~ inf
2. 环境

   1. state：每个变量离散化为6个bins，共计$6^4$个
   2. action：left_shift, right_shift两个
   3. Q矩阵：$size=6^4*2$

## 解决方案

1. Tools：
   1. GetQ
   2. GetArgmax
   3. UpdateQbyR
2. Q学习

## 修改内容

1. Agent：开发时使用随机agent，上线使用讯飞agent
2.
