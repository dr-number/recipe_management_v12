# Initial setup
    docker-compose -f docker-compose.local.yml --env-file .env.local up --build
    docker exec -ti recipe_management_web python3 manage.py makemigrations
    docker exec -ti recipe_management_web python3 manage.py migrate
    docker exec -ti recipe_management_web python3 manage.py collectstatic
    docker exec -ti recipe_management_web python3 manage.py seed_users

# shell_plus
    docker exec -ti recipe_management_web python3 manage.py shell_plus --notebook

# For editing files created using the django application
sudo chown -R  $USER:$USER path_to_dir

# Start shell
docker exec -ti recipe_management_web python3 manage.py shell

# Seed users
    docker exec -ti recipe_management_web python3 manage.py seed_users
