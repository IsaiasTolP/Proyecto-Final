from rest_framework import serializers
from .models import Project, ProjectCategory, ProjectImage
from users.serializers import UserSerializer

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'
        read_only_fields = ['owner']

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
        )
        read_only_fields = ['start_date']

    def create(self, validated_data):
        images_data = validated_data.pop('project_images', [])
        project = Project.objects.create(**validated_data)
        if images_data:
            for image_data in images_data:
                ProjectImage.objects.create(project=project, **image_data)
        else:
            ProjectImage.objects.create(project=project)
        return project

class SimpleProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner')