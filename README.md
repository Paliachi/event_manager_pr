# **Event Manager Test PR**

### Starting the project locally:
* Clone repository on the local machine:
    * [LINK to REPOSITORY on GitHub](https://github.com/Paliachi/event_manager_pr)
* Enter in root repository if needed
    * `cd event_manager_pr/`
* Open terminal and type: `make build`
* Wait until you see: Starting development server at http://0.0.0.0:8000/
* Follow this link and utilize swagger
  * [SWAGGER LINK](http://0.0.0.0:8000/schema/swagger-ui/)

### Running Tests:

* open a new terminal
* enter in root repository
* type in terminal: `make tests`

### Utilizing Swagger:
* Register User.
* Login with those credentials.
* Copy the access token from response data.
* Press "Authorize"(upper write corner) button and paste the access token in.
* After this procedure all endpoints which require authentication will be accessible.  
* If you want to change user, log out using "Authorize" button and log in with different user.
