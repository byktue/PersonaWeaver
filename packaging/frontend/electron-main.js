// PersonaWeaver 前端 Electron 主进程
// 作用：把 Vite 构建出的 SPA（dist/）装进桌面壳，打成绿色 exe。
// 数据/配置由前端自身走 localStorage 与 .env 注入的后端地址，Electron 不额外落 C 盘。
const { app, BrowserWindow, shell } = require("electron");
const path = require("path");

// 允许通过环境变量覆盖后端地址（前端页面通过 settings 读取；这里仅示意可配置）
const BACKEND_URL = process.env.PERSONAWEAVER_BACKEND || "http://127.0.0.1:8000";

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 860,
    title: "PersonaWeaver",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // 外部链接用系统浏览器打开，避免在应用内跳走
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("http")) {
      shell.openExternal(url);
      return { action: "deny" };
    }
    return { action: "allow" };
  });

  // 加载打包进来的 SPA 首页
  win.loadFile(path.join(__dirname, "dist", "index.html"));
}

app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
