import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const distDir = path.join(__dirname, "dist");
const portalDir = path.join(distDir, "portal");

const app = express();

// Serve portal static pages first
app.use(
  "/portal",
  express.static(portalDir, {
    index: "index.html",
    extensions: ["html"],
  })
);

// Serve main app static assets
app.use("/assets", express.static(path.join(distDir, "assets")));
app.use("/brand", express.static(path.join(distDir, "brand")));
app.use(express.static(distDir));

// Ensure /portal and /portal/ both work
app.get("/portal", (req, res) => {
  res.sendFile(path.join(portalDir, "index.html"));
});

// Do NOT SPA-fallback /portal/* to the React app.
// If a portal file isn't found, return 404.
app.get("/portal/*", (req, res) => {
  res.status(404).send("Not Found");
});

// React landing page is single-route ("/"); return index.html for everything else
// to avoid platform 404s on refresh.
app.get("*", (req, res) => {
  res.sendFile(path.join(distDir, "index.html"));
});

const port = Number(process.env.PORT || 3000);
app.listen(port, "0.0.0.0", () => {
  console.log(`Frontend listening on :${port}`);
});
