# 🏭 Industrial Inspection Platform

> 基于 FastAPI + React 的工业检验数据管理平台

## ✨ 功能特性

- 用户角色管理（Admin/Member/Visitor）
- 多项目支持（Admin可创建项目并分配存储空间）
- 材料检验记录管理
- 组对（Fit-up）记录管理
- 最终焊接检验记录（继承组对数据）
- NDT请求单（RFI）管理
- 响应式前端表格（增删改查）
- JWT认证 + 角色权限控制
- Docker一键部署

## 🚀 快速启动

```bash
# 克隆项目
git clone https://github.com/yourname/industrial-inspection-platform.git
cd industrial-inspection-platform

# 启动服务
docker-compose up --build

# 访问
Frontend: http://localhost:3000
Backend API: http://localhost:8000/docs