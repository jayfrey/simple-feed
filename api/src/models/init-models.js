var DataTypes = require("sequelize").DataTypes;
var _articles = require("./articles");

function initModels(sequelize) {
  var articles = _articles(sequelize, DataTypes);


  return {
    articles,
  };
}
module.exports = initModels;
module.exports.initModels = initModels;
module.exports.default = initModels;
