const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json()); // To support JSON-encoded bodies
app.use(
  bodyParser.urlencoded({
    // To support URL-encoded bodies
    extended: true,
  })
);

const routes = require("./api/routes");
routes(app);

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
