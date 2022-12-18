const Sequelize = require('sequelize');
module.exports = function(sequelize, DataTypes) {
  return sequelize.define('articles', {
    id: {
      autoIncrement: true,
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true
    },
    title: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    image_url: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    published_date: {
      type: DataTypes.STRING(20),
      allowNull: true
    },
    publisher_name: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    html_content: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    page_url: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    category_tags: {
      type: DataTypes.ARRAY(DataTypes.TEXT),
      allowNull: true
    },
    topic: {
      type: DataTypes.STRING(255),
      allowNull: true
    },
    tags: {
      type: DataTypes.ARRAY(DataTypes.TEXT),
      allowNull: true
    },
    source: {
      type: DataTypes.STRING(255),
      allowNull: true
    }
  }, {
    sequelize,
    tableName: 'articles',
    schema: 'public',
    hasTrigger: true,
    timestamps: true,
    indexes: [
      {
        name: "articles_pkey",
        unique: true,
        fields: [
          { name: "id" },
        ]
      },
    ]
  });
};
