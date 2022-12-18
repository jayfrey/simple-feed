const express = require("express");
const articleRouter = express.Router();
const ArticleController = require("./controllers/ArticleController");

const statusCodes = require("http").STATUS_CODES;
const httpConstants = require("http2").constants;

module.exports = (app) => {
  app.get("/", (req, res) => {
    res
      .status(httpConstants.HTTP_STATUS_OK)
      .send(statusCodes[httpConstants.HTTP_STATUS_OK]);
  });

  app.get("/healthcheck", (req, res) => {
    res
      .status(httpConstants.HTTP_STATUS_OK)
      .send(statusCodes[httpConstants.HTTP_STATUS_OK]);
  });

  articleRouter.route("/").get(ArticleController.index);
  articleRouter.route("/latest").get(ArticleController.getLatestArticles);
  app.use("/articles", articleRouter);
};
