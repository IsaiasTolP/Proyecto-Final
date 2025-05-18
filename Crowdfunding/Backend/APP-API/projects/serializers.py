from rest_framework import serializers
from .models import Project, ProjectCategory, ProjectImage
from users.serializers import SimpleUserSerializer

class ProjectCategorySerializer(serializers.ModelSerializer):
    num_projects = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProjectCategory
        fields = ['id', 'category', 'icon', 'color', 'num_projects']


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    project_images = ProjectImageSerializer(many=True, required=False)
    total_donated = serializers.ReadOnlyField()
    percent_completed = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'goal',
            'start_date', 'is_active',
            'category', 'owner', 'project_images',
            'total_donated', 'percent_completed',
            'featured',
        )
        read_only_fields = ['start_date']

class SimpleProjectSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner')