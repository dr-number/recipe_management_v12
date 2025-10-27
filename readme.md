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


Chef
## list all recipe categories
    curl -X GET \
      'http://localhost:8700/main/lk_chef/list_all_recipe_categories/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: token MyToken'