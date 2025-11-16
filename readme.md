# Task
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/task-1.png">
   </p>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/task-2.png">
   </p>
</figure>

# Initial setup in Docker
    docker-compose -f docker-compose.local.yml --env-file .env.local up --build
    docker exec -ti recipe_management_web python3 manage.py makemigrations
    docker exec -ti recipe_management_web python3 manage.py migrate
    docker exec -ti recipe_management_web python3 manage.py collectstatic

# Initial setup in venv
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8700

# Url Swagger
http://localhost:8700/swagger_doc/

# Create user admin
    docker exec -ti recipe_management_web python3 manage.py seed_users

## Url admin panel
http://localhost:8700/admin/login/?next=/admin/

## login
    The value of the variable ADMIN_LOGIN in file .env.local

## Password
    The value of the variable ADMIN_PASSWORD in file .env.local

# Run shell_plus
    docker exec -ti recipe_management_web python3 manage.py shell_plus --notebook

# Run shell
    docker exec -ti recipe_management_web python3 manage.py shell

# For editing files created using the django application
    sudo chown -R  $USER:$USER path_to_dir

# Debuger
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/django_debugger_visual_studio_code.png">
      <p align="center">Django debugger in Visual Studio Code in a Docker container</p>
   </p>
</figure>

# Admin panel
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/chef_and_admin.png">
      <p align="center">Permission in admin panel</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/filter_raiting.png">
      <p align="center">Filter raiting</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/filter_type_and_time.png">
      <p align="center">Filter type and time</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/filter_types_and_raitings.png">
      <p align="center">Filter type and raiting</p>
   </p>
</figure>

# Test send email
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/test_send_email_from_jupiter_notebook.png">
      <p align="center">Test send email from jupiter notebook in localhost</p>
   </p>
</figure>


# Pages
http://localhost:8700/main/front/register/

http://localhost:8700/main/front/loginin/

http://localhost:8700/main/front/add_recipe/

http://localhost:8700/main/front/edit_account/


# CURLs

Registration and login
## create account
    curl -X POST \
      'http://localhost:8700/main/allow_any/create_account/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "email": "dr.number@yandex.ru",
      "first_name": "Иванов",
      "last_name": "Иван",
      "password": "MyPassword0",
      "password2": "MyPassword0",
      "type": "user_type_chef"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/registration_error_user_already_exist.png">
      <p align="center">Registration error user already exist</p>
   </p>
</figure>

## check confirmation code
    curl -X POST \
      'http://localhost:8700/main/allow_any/check_confirmation_code_id/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "user_id": 30,
      "code": "2519"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/success_registration.png">
      <p align="center">Success registration</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/error_echeck_code_and_report_to_tg_bot.png">
      <p align="center">Error echeck code and report to bot</p>
   </p>
</figure>

## update confirmation code
    curl -X POST \
      'http://localhost:8700/main/allow_any/update_confirmation_code_id/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "user_id": 30
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/registration_and_update_conformation_code.png">
      <p align="center">Registration and update conformation code</p>
   </p>
</figure>

## login
    curl -X POST \
      'http://localhost:8700/main/allow_any/login/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "email": "dr.number@yandex.ru",
      "password": "MyPassword0"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/error_login.png">
      <p align="center">Error login</p>
   </p>
</figure>


For all users

## get user info
    curl -X GET \
      'http://localhost:8700/main/lk_all/get_user_info/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/get_user_info.png">
      <p align="center">User info</p>
   </p>
</figure>

## list all recipes
    curl -X GET \
      'http://localhost:8700/main/lk_all/list_all_recipes/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/list_all_recipes.png">
      <p align="center">list all recipes</p>
   </p>
</figure>

## get recipe
    curl -X GET \
      'http://localhost:8700/main/lk_all/get_recipe/?id=4' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

## add comment to recipe
    curl -X POST \
      'http://localhost:8700/main/lk_all/add_comment_to_recipe/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken' \
      --data-raw '{
      "id_recipe": 4,
      "raiting": 5,
      "text": "Очень вкусно"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/notification_comment.png">
      <p align="center">Notification comment</p>
   </p>
</figure>

## get my comments
    curl -X GET \
    'http://localhost:8700/main/lk_all/get_list_my_comments/' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: token MyToken'

## add recipe to favorite
    curl -X POST \
      'http://localhost:8700/main/lk_all/add_recipe_to_favorite/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken' \
      --data-raw '{
      "id": 4
    }'

## get list my favorites
    curl -X GET \
      'http://localhost:8700/main/lk_all/get_list_my_favorites/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

## edit profile
      curl -X POST \
      'http://localhost:8700/main/lk_all/edit_profile/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken' \
      --data-raw '{
      "first_name": "Сидоров"
      }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/edit_profile.png">
   </p>
</figure>

For Chef
## list all recipe categories
    curl -X GET \
      'http://localhost:8700/main/lk_chef/list_all_recipe_categories/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

## add recipe
    curl -X POST \
      'http://localhost:8700/main/lk_chef/add_recipe/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken' \
      --data-raw '{
      "title": "Грибной суп",
      "ingredients": "Грибы, мясо, картошка, лук",
      "steps": "Берем и готовим",
      "id_category_recipe": 2,
      "time_cooking": "00:30:00",
      "html_description": "<p><img src=\"data:image/jpeg;base64,/9j/4......KR3qwN5UXqf//Z\"></p>"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/add_recipe.png">
      <p align="center">Add recipe</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/add_recipe_in_admin.png">
      <p align="center">New recipe in admin</p>
   </p>
</figure>

## update recipe
    curl -X POST \
      'http://localhost:8700/main/lk_chef/update_recipe/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken' \
      --data-raw '{
      "id": 4,
      "title": "Грибной суп",
      "ingredients": "Грибы, мясо, картошка, лук",
      "steps": "Берем и готовим",
      "id_category_recipe": 2,
      "time_cooking": "00:30:00",
      "html_description": "<p><img src=\"data:image/jpeg;base64,/9j/4......KR3qwN5UXqf//Z\"></p>"
    }'

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/recipe_management_v12/blob/master/for_readme/img/notification_edit_recipe.png">
      <p align="center">Notification edit recipe</p>
   </p>
</figure>
