========================================================
 PersonaWeaver 前端打包工作区  说明
========================================================

本目录（packaging/frontend）是【前端 Electron 打包工作区】。
它把 Vue 前端界面装进桌面壳，打成绿色免安装 exe。

--------------------------------------------------------
【两种交付形态】
--------------------------------------------------------

形态①：只给成品 exe（别人双击即用，不自己打包）
  → 交付 release\win-unpacked\ 整个文件夹
  → 配置已编译进 exe，别人无需任何配置文件，双击 PersonaWeaver.exe 即用
  → 前提：先启动后端（personaweaver-backend）

形态②：给可重新打包的工作区（别人要改配置/界面重新打包）
  → 交付本目录（packaging/frontend）+ 前端源码（CharPick-frontend 分支）
  → 别人改 .env.local 后，运行 build_frontend.ps1 重新打包

--------------------------------------------------------
【关键：前端配置怎么改】（和后端不同！）
--------------------------------------------------------

前端配置是【构建时】编译进 exe 的，不是运行时读文件。
所以：
  - exe 成品旁边放 .env.local 【无效】，它不会去读
  - 改配置 = 改 .env.local，然后【重新构建+打包】

配置文件：
  - .env.local          真实配置（本地/内部用，含密钥，勿公开）
  - .env.local.example  占位模板（公开分发时给这份，让对方填自己的）

配置项（详见 .env.local.example）：
  VITE_BACKEND_URL           后端地址
  VITE_SUPABASE_*            Supabase（anon key 可公开）
  VITE_OSS_*                 阿里云 OSS（AccessKeySecret 敏感！）

--------------------------------------------------------
【重新打包步骤】
--------------------------------------------------------
1. 首次：复制 .env.local.example 为 .env.local，填入真实值
2. 运行：powershell -ExecutionPolicy Bypass -File build_frontend.ps1
3. 产物：release\win-unpacked\PersonaWeaver.exe

脚本会自动：用 .env.local 构建前端 → 打包 exe → 手动重建 asar（修缓存 bug）

--------------------------------------------------------
【安全警告】
--------------------------------------------------------
- OSS AccessKeySecret 是敏感凭据。含真实值构建的 exe / 本目录 .env.local
  【绝不能】上传公开仓库或公开 Release。
- 公开分发时：用 .env.local.example（占位），让使用者填自己的密钥。
- Supabase anon key 是设计上可公开的前端密钥，风险较低。
