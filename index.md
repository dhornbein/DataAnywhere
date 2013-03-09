---
layout: home
title: Home
---

## Summary

The Data Anywhere project was developed at the [#OccupyDataNYC Hackathon][1] on March 1st & 2nd. Read the [project outline][2]. It is currently being tested for use with Hurricane Sandy relief around New York City as part of [#OccupySandy][3].

### The problem

There are many relief and rebuilding focused organizations collecting data. This data needs to be both **shared with collaborators** and **secure, to protect private information**.

Currently data is stored in many (mainly proprietary) software packages, if it is even digitized at all. Data stewards don't have good ways to share public data while keeping private data secure. 

You can read more about this project on [Drew's Blog][4].

## Solution

Data Anywhere seeks to provide a simple, extend-able, single focus solution to storing, securing, and sharing any kind of data.

Here's a vague diagram outlining the collection of paper forms:  
![Data Anywhere diagram](http://blog.dhornbein.com/wp-content/uploads/2013/03/dataanywhere_workflow_draf1.png)

1. Data is collected with a form based on community needs and collective data standards.
2. Data is entered into a computer, digitized. If information is collected digitally this step is simplified.
3. Data is mapped to a standardized format for storage. Structuring input data to match standards will simplify this process.
4. Data is stored in an off-the-shelf server.
5. A data API is developed to manipulate stored data. Data stewards control how data is made available. By following collective standards uniform data can be distributed to a network of data servers.
6. App authors can access shared data from the server network to run services.
7. Apps can interface with other systems both open and closed.

### The system

Data Anywhere can be broken down into three distinct sections:

1. **Server Setup** - Data stewards will need to configure a VPS (virtual private server)
2. **Data import** - Taking non standard data from bizarre sources (initially with a focus on `.csv`) and import them into a **standardized** MongoDB data structure.
3. **RESTful API development** - Using Python with Flask simple standardized API will need to be customized depending on the data.

Each step will initially be very hands on. As standards are developed common libraries can be created to manage each step.

## [Server Setup](./server_setup.html)

The current strategy is to set up an off-the-shelf VPS server running either Ubuntu or Fedora.

Detailed instructions on [server setup](./server_setup.html)

## [Data Import](./data_import.html)

Data import

[1]: http://occupydatanyc.org/2013/03/03/data-anywhere-project-hackathon-day-two/
[2]: http://occupydatanyc.org/2013/02/12/open-data-project/
[3]: http://occupysandy.org
[4]: http://blog.dhornbein.com/2013/03/07/data-anywhere-distributed-data-storage-and-sharing-solution/