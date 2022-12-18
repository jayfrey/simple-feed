const db = require("../../models/index");
const initModels = require("../../models/init-models");
const models = initModels(db.sequelize);
const { Op } = require("sequelize");
const moment = require("moment");
const statusCodes = require("http").STATUS_CODES;
const httpConstants = require("http2").constants;

const controllers = {
  index(req, res) {
    res
      .status(httpConstants.HTTP_STATUS_OK)
      .send(statusCodes[httpConstants.HTTP_STATUS_OK]);
  },

  async getLatestArticles(req, res) {
    const articles = await models.articles.findAll({
      where: {
        published_date: { [Op.lte]: moment().format("YYYY-MM-DD HH:mm:ss") },
      },
      order: [["published_date", "DESC"]],
      limit: 5,
      raw: true,
    });

    res.status(httpConstants.HTTP_STATUS_OK).json(articles);
  },
};

module.exports = controllers;
