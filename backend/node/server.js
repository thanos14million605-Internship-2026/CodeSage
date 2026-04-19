const path = require("path");
const express = require("express");
const app = require("./app");
const { pool } = require("./config/database");

if (process.env.NODE_ENV === "production") {
  const frontendPath = path.join(__dirname, "..", "..", "frontend", "dist");

  app.use(express.static(frontendPath));

  app.get("*", (req, res) => {
    res.sendFile(path.join(frontendPath, "index.html"));
  });
}

const PORT = process.env.PORT || 5000;

// Start server
app.listen(PORT, async () => {
  console.log(`🚀 CodeSage Backend Server running on port ${PORT}`);

  // Test database connection
  try {
    const client = await pool.connect();
    console.log("✅ Database connected successfully");
    client.release();
  } catch (error) {
    console.error("❌ Database connection failed:", error.message);
  }
});

// Graceful shutdown
process.on("SIGTERM", async () => {
  console.log("SIGTERM received, shutting down gracefully");
  await pool.end();
  process.exit(0);
});

process.on("SIGINT", async () => {
  console.log("SIGINT received, shutting down gracefully");
  await pool.end();
  process.exit(0);
});
