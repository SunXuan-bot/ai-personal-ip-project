import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const sourceDir = path.join(root, "custom");
const pptDir = path.join(root, "ppt");
const assetDir = path.join(pptDir, "assets", "user-custom");
const htmlFile = path.join(pptDir, "index.html");

mkdirSync(assetDir, { recursive: true });
copyFileSync(path.join(sourceDir, "green-editable.css"), path.join(assetDir, "green-editable.css"));
copyFileSync(path.join(sourceDir, "green-editable.js"), path.join(assetDir, "green-editable.js"));

let html = readFileSync(htmlFile, "utf8");
html = html.replace(/\n?<!-- OPC_GREEN_EDITABLE_START -->[\s\S]*?<!-- OPC_GREEN_EDITABLE_END -->\n?/g, "\n");
const injection = `
<!-- OPC_GREEN_EDITABLE_START -->
<link rel="stylesheet" href="assets/user-custom/green-editable.css">
<script src="assets/user-custom/green-editable.js"></script>
<!-- OPC_GREEN_EDITABLE_END -->
`;
html = html.replace("</body>", `${injection}</body>`);
writeFileSync(htmlFile, html);
console.log(`已注入 OPC v3 局部样式：${htmlFile}`);
