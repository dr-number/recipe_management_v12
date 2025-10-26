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