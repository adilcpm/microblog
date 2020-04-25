# MICROBLOG
Project Built as the end product of my Flask Learning from [The Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

Progress : 90%

**Features**

1.Users can write Posts

2.User Following System

3.User Private Messages

4.Full Text Search using Elastic Search

5.API[Now enabled only for User Model, will be extended to Post Model]

**API Endpoints**

1.Get Token: /api/tokens

  * GET {username}:{password}, to get new token

  * DELETE, to delete token 

  >Token must be passed as "Bearer {token}" for all subsequent requests except Creating New User endpoint

2.Endpoints
  
  **Users**
  1. GET /api/users/{id}
  >get details of User with ID={id}
  2. GET /api/users
  >get details of All User
  3. GET /api/users/{Id}/followers
  >return followers of User with ID={id}
  4. GET /api/users/{id}/followed
  >return users following the User with ID={id>}
  5. GET /api/users/{id}/posts
  >return posts of the user with ID={id}
  6. POST /api/users
  >Register a new account, which returns the User Details on succesfull transaction
  7. PUT /api/users/{id}
  >modify Username, Email, About Me of User, by passing it as JSON data
 
  **Posts**
  1.GET /api/posts
  >get all posts sorted by timestamp descending
  2.GET /api/posts/{id}
  >get post with id={id}
  3.POST /api/posts
  >Create new post with passing {"body" : "data"} JSON format
