# Who Really?!

Sometimes it's hard to know yourself. Good thing there's Who Really?! It uses Neural Network classifiers to tell the gender, age and ethnicity of a portrait you give it. Sometimes it's right, sometimes you just don't know that it is.

## Code

This repo acts as the hub to the project. To increase maintainabilty and modularity, the real code is split among the following repos:

### [who-really-classifiers](https://github.com/jonasmerlin/who-really-classifiers)

Here is where the data meet the neural nets and both combine to form beautiful classifiers. Uses multi-class transfer learning of top performing image net architectures.

### [who-really-server](https://github.com/jonasmerlin/who-really-server)

The server provides the API endpoints for clients to interact with the classifiers. Currently there are three endpoints: one to upload a portrait to, one which expects a URL and one specifically for our Slack slash command.

It automatically gets deployed to heroku on pushes, but you can also pull it yourself and run it locally.

### [who-really-website](https://github.com/jonasmerlin/who-really-website)

The code for our website. Either upload a file yourself or provide a URL. If you run the server locally, pull this repo and switch over to the local branch as well to interact with the server on localhost.

### [who-really-cli](https://github.com/jonasmerlin/who-really-cli)

A basic CLI for Who Really?! Interacts with the API via HTTP requests.

### [who-really-notebooks](https://github.com/jonasmerlin/who-really-notebooks)

Here you can find a few jupyter notebooks we initally made to help those on the team with no prior machine learning experience learn.
