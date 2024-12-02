
# Start the Tailwind Dev Server

python manage.py tailwind start


This will compile your Tailwind CSS files and watch for changes.


Before deploying your project, collect the static files:


python manage.py collectstatic


Run the following command to generate optimized CSS for production:


python manage.py tailwind build

