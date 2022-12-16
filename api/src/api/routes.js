const controller = require("./controllers");

module.exports = (app) => {
  app.get("/", controller.index);
  app.get("/ping", controller.ping);

  // Creates the endpoint for our webhook
  // app.post("/webhook", controller.handle_webbook);

  // Adds support for GET requests to our webhook
  // app.sget("/webhook", controller.verify_webhook);
};
