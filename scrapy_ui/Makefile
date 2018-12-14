createsuperuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'qwer4321');" | python3 manage.py shell

build:
	docker build -t devopszcom/scrapy_ui:0.1.0 .