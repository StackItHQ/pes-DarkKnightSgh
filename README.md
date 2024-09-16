# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [ ] My code's working just fine! 🥳
- [ ] I have recorded a video showing it working and embedded it in the README ▶️
- [ ] I have tested all the normal working cases 😎
- [ ] I have even solved some edge cases (brownie points) 💪
- [ ] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.

## Developer's Section
*Add your video here, and your approach to the problem (optional). Leave some comments for us here if you want, we will be reading this :)*





## Google Sheets and MySQL Synchronization

This project provides a solution for real-time synchronization between Google Sheets and a MySQL database. The application ensures that any CRUD operations (Create, Read, Update, Delete) performed on either platform are mirrored across both systems, maintaining data consistency.

### Features:
Real-time Synchronization: Automatically syncs data between Google Sheets and MySQL database.
CRUD Operations: Supports Create, Read, Update, and Delete operations.

### Architecture and Components
- Flask Web Server:
Acts as the core of the synchronization system, handling HTTP requests and responses.
Provides endpoints for synchronization, adding records, deleting records, and retrieving data.

- Google Sheets Integration:
Utilizes the Google Sheets API to interact with Google Sheets.
Handles reading data from and writing data to Google Sheets.
Synchronizes data from Google Sheets to MySQL and vice versa.

-MySQL Database:
Stores data that is synchronized with Google Sheets.
Schema includes tables designed to match the structure of data in Google Sheets.

### Description:
 The idea for using Flask was inspired by my microservices project, and I sought assistance from ChatGPT for implementing the synchronization logic. The primary goal was to ensure that any CRUD (Create, Read, Update, Delete) operations performed on either Google Sheets or the MySQL database would be reflected in both systems in real-time.

Synchronization Mechanism:
- Flask Application: A Flask application was built to handle synchronization tasks between Google Sheets and the MySQL database.
- CRUD Operations: The application supports all CRUD operations. Records can be added, updated, and deleted from both Google Sheets and the MySQL database.
- Real-time Sync: Synchronization occurs every 10-30 seconds. This interval was chosen to balance between real-time updates and API quota limits.
  
### Challenges:
API Quota Management: To address the issue of exceeding API quotas, the sync interval was adjusted to reduce the number of read requests. Additionally, optimizations were made to ensure efficient use of API resources.

It was working properly,but unfortunately i could not record while it was working,iam unable to fix the api issue
## Video : 
https://drive.google.com/file/d/1pBBku3CCzk-K7kZKE19yzgvz7S8m_TPK/view?usp=sharing





