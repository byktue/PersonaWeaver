// PersonaWeaver 前端 Electron 主进程
// 作用：把 Vite 构建的 SPA（dist/）通过内置本地 HTTP 服务提供，再用 Electron 窗口加载。
// 为什么用本地 HTTP 而非 file://：
//   1) 前端用 Vue Router 的 createWebHistory（history 模式），file:// 下无法工作；
//   2) file:// 下 SPA 路由回退（找不到路径回 index.html）也无法实现。
// 内置 http 服务解决这两点，且只监听 127.0.0.1 随机端口，纯本地、不占 C 盘。
const { app, BrowserWindow, shell } = require("electron");
const http = require("http");
const fs = require("fs");
const path = require("path");

const DIST_DIR = path.join(__dirname, "dist");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".map": "application/json; charset=utf-8",
};

function startStaticServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let urlPath = decodeURIComponent(req.url.split("?")[0]);
      if (urlPath === "/") urlPath = "/index.html";
      let filePath = path.join(DIST_DIR, urlPath);

      // 防目录穿越
      if (!filePath.startsWith(DIST_DIR)) {
        res.writeHead(403);
        res.end("Forbidden");
        return;
      }

      const ext = path.extname(filePath).toLowerCase();

      const sendFile = (fp) => {
        // 用读取尝试而非 fs.existsSync：asar 内 existsSync 不可靠，
        // 但 readFile 能正确读 asar 归档内的文件。
        fs.readFile(fp, (err, data) => {
          if (err) {
            // 静态资源（有扩展名如 .js/.css）读不到 → 真正 404，
            // 绝不能回退到 index.html，否则 JS 收到 HTML 会报 Unexpected token '<'。
            if (ext && ext !== ".html") {
              res.writeHead(404);
              res.end("Not found");
              return;
            }
            // 无扩展名的路径（SPA 路由）→ 回退到 index.html
            fs.readFile(path.join(DIST_DIR, "index.html"), (e2, html) => {
              if (e2) {
                res.writeHead(500);
                res.end("Internal error: " + e2.message);
                return;
              }
              res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
              res.end(html);
            });
            return;
          }
          res.writeHead(200, { "Content-Type": MIME[path.extname(fp).toLowerCase()] || "application/octet-stream" });
          res.end(data);
        });
      };

      sendFile(filePath);
    });
    // 端口 0 = 系统分配空闲端口，仅本地
    server.listen(0, "127.0.0.1", () => {
      resolve(server.address().port);
    });
  });
}

function createWindow(port) {
  const win = new BrowserWindow({
    width: 1280,
    height: 860,
    title: "PersonaWeaver",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      // 桌面应用直连 vivo/ECNU 等外部 LLM API 属跨域请求，浏览器 CORS 会拦截；
      // 本地可信桌面壳关闭 webSecurity 以允许直连（不加载不可信远程页面，风险可控）。
      webSecurity: false,
    },
  });

  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("http")) {
      shell.openExternal(url);
      return { action: "deny" };
    }
    return { action: "allow" };
  });

  win.loadURL(`http://127.0.0.1:${port}/`);
}

app.whenReady().then(async () => {
  const port = await startStaticServer();
  createWindow(port);
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow(port);
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
