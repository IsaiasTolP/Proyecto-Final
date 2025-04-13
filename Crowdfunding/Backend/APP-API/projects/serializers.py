from rest_framework import serializers
from .models import Project, ProjectCategory, ProjectImage

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer()
    project_images = ProjectImageSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['start_date']