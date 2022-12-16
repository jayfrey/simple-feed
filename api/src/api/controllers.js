const db = require("../models/index");

// const fbConfig = require("../configs/fb");
// const RequestSendAPI = require("../services/request-send-api");
// const Response = require("../services/response");
// const GraphApi = require("../services/graph-api");
// const MessageHandler = require("../services/message-handler");

const controllers = {
  index(req, res) {
    res.status(200).send("");
  },

  ping(req, res) {
    res.status(200).send("pong");
  },

  // verify_webhook(req, res) {
  //   // Your verify token. Should be a random string.
  //   let VERIFY_TOKEN = fbConfig.verifyToken;

  //   // Parse the query params
  //   let mode = req.query["hub.mode"];
  //   let token = req.query["hub.verify_token"];
  //   let challenge = req.query["hub.challenge"];

  //   // Checks if a token and mode is in the query string of the request
  //   if (mode && token) {
  //     // Checks the mode and token sent is correct
  //     if (mode === "subscribe" && token === VERIFY_TOKEN) {
  //       // Responds with the challenge token from the request
  //       console.log("WEBHOOK_VERIFIED");
  //       res.status(200).send(challenge);
  //     } else {
  //       // Responds with '403 Forbidden' if verify tokens do not match
  //       res.sendStatus(403);
  //     }
  //   }
  // },

  // handle_webbook(req, res) {},
};

module.exports = controllers;
