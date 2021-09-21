# turnio-data-export-replit

An example Turn.io data export Replit. This shows how to export data from the [Turn Data Export API](https://whatsapp.turn.io/docs/index.html#data-export-api) and apply scrubbing rules if desired.

*This Replit assumes the following*:

1. You have gone through earlier examples (like perhaps the [webhooks example](https://github.com/turnhub/turnio-webhooks-replit)) and are comfortable with how to get an authentication token for Turn and set it up as a secret in Repl.it

# How to run this Repl.it

[![Run on Repl.it](https://repl.it/badge/github/turnhub/turnio-data-export-replit)](https://repl.it/github/turnhub/turnio-data-export-replit)

1. Click the `Run on Repl.it` button above and install this example into your Repl.it workspace.
2. Get a Turn token and add it as a secret called `TOKEN` in Repl.it
3. Send and receive some messages on your Turn.io number
4. Hit `Run` in your replit and see the messages from the last 24 hours listed in your Repl.it console with the scrubbing rules applied.