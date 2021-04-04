const Pusher = require("pusher");

export default async function mainHandler(event, data) {

  const pusher = new Pusher({
    appId: "1182764",
    key: process.env.PUSHER_KEY,
    secret: process.env.PUSHER_SECRET,
    cluster: "ap1",
    useTLS: true,
  });

  await pusher.trigger('drama', event, data ? data : {});

  return("Success");

}
