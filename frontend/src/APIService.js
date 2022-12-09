const https = require("https");
const http = require("http");

const useHTTPS = false;

exports.uploadDesign = (data) => {
  const postData = JSON.stringify(data);

  const options = {
    path: "/api/upload-design",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": postData.length,
    },
  };

  const client = useHTTPS ? https : http;

  return new Promise((resolve, reject) => {
    const request = client.request(options, (res) => {
      if (res.statusCode != 200) reject(res.statusCode);

      res.on("data", resolve);
    });

    request.on("error", (e) => {
      console.error(e);
      reject(e);
    });

    request.write(postData);
    request.end();
  });
};
