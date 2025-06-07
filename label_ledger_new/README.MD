# Label Ledger

### Overview

Label Ledger is a project that allows you to create a downloadble label with current news topics. A mini-newspaper of sorts.

### Stack:

- This project is primarily built with Next.js, and Tailwind CSS and hosted in a Docker Container.
- We're using The News API to get the top 3 stories. Documentation can be found [here](https://www.thenewsapi.com/documentation).
- The docker container shares a port 3000 with the host machine and is set up with a docker-compose file.

### User Workflow:

1. User visits the website.
2. User clicks on the "Make my LabelLedger" button.
3. User clicks on the "Generate" button.
4. User is directed to a page with the label.
5. User can download or print the label from their browser.

### Program Workflow:

1. User submits the form with a topic.
2. The program makes a request to the News API to get the top 3 stories.
3. The program creates a label with the top 3 stories and the summary. This is 4x6 inches in size. There should be a title at the top, with the selected topic. The top 3 stories should be listed in a column, with the summary below each headline. The label should be saved as a PDF.
4. The program returns the label to the user on the website to download or print.

### Setup:

- Clone the repository
- Run `docker-compose up --build` to start the container.
- Open the project in your browser at `http://localhost:3000`
