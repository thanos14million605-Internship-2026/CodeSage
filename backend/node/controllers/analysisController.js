const axios = require("axios");
const History = require("../models/History");
const { body, validationResult } = require("express-validator");

const analyzeCode = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { code, repo_url } = req.body;

    if (!code && !repo_url) {
      return res
        .status(400)
        .json({ error: "Either code or repo_url must be provided" });
    }

    // Call FastAPI service
    try {
      const fastapiResponse = await axios.post(
        `${process.env.FASTAPI_URL}/api/analyze`,
        { code, repo_url },
        { timeout: 30000 } // 30 second timeout
      );

      const analysisResult = fastapiResponse.data;

      // Save to history
      const historyEntry = await History.create({
        user_id: req.user.id,
        file_name: repo_url ? "repository_analysis" : "uploaded_file.py",
        repo_url: repo_url || null,
        risk_score: analysisResult.overall_risk_score,
        result_json: analysisResult,
      });

      res.json({
        message: "Analysis completed successfully",
        result: analysisResult,
        history_id: historyEntry.id,
      });
    } catch (apiError) {
      console.log(apiError);
      console.error("FastAPI Error:", apiError.message);

      if (apiError.code === "ECONNREFUSED") {
        return res.status(503).json({
          error:
            "Analysis service is temporarily unavailable. Please try again later.",
        });
      }

      if (apiError.response) {
        return res.status(apiError.response.status).json({
          error: apiError.response.data.detail || "Analysis failed",
        });
      }

      throw apiError;
    }
  } catch (error) {
    console.error("Analysis Error:", error);
    res.status(500).json({ error: "Failed to analyze code" });
  }
};

const validateAnalysis = [
  body("code")
    .optional()
    .isLength({ min: 1 })
    .withMessage("Code cannot be empty if provided"),
  body("repo_url")
    .optional()
    .isURL()
    .withMessage("Repository URL must be valid"),
];

module.exports = {
  analyzeCode,
  validateAnalysis,
};
