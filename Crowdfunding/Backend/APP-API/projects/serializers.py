from rest_framework import serializers
from .models import Project, ProjectCategory, ProjectImage

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
        fields = [
            'id', 'name', 'description', 'goal',
            'start_date', 'is_active',
            'category', 'owner', 'project_images',
            'total_donated', 'percent_completed',
        ]
        read_only_fields = ['start_date']