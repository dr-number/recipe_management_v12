# Initial setup
    docker-compose -f docker-compose.local.yml --env-file .env.local up --build
    docker exec -ti recipe_management_web python3 manage.py makemigrations
    docker exec -ti recipe_management_web python3 manage.py migrate
    docker exec -ti recipe_management_web python3 manage.py collectstatic

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


# Pages
    http://localhost:8700/main/front/register/

    http://localhost:8700/main/front/loginin/


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

## check confirmation code
    curl -X POST \
      'http://localhost:8700/main/allow_any/check_confirmation_code_id/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "user_id": 30,
      "code": "2519"
    }'

## update confirmation code
    curl -X POST \
      'http://localhost:8700/main/allow_any/update_confirmation_code_id/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "user_id": 30
    }'

## login
    curl -X POST \
      'http://localhost:8700/main/allow_any/login/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "email": "dr.number@yandex.ru",
      "password": "MyPassword0"
    }'


For all users
## list all recipes
    curl -X GET \
      'http://localhost:8700/main/lk_all/list_all_recipes/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'

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