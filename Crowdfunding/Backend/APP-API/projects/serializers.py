from rest_framework import serializers
from .models import Project, ProjectCategory, ProjectImage, ProjectSponsorship
from users.serializers import SimpleUserSerializer
from PaymentMethod.models import PaymentMethod

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

class ProjectSponsorshipSerializer(serializers.ModelSerializer):
    cvv = serializers.CharField(write_only=True, max_length=4, min_length=3)

    class Meta:
        model = ProjectSponsorship
        fields = '__all__'
        read_only_fields = ['id', 'date', 'user', 'amount']

    def validate_payment_method(self, value: PaymentMethod):
        request = self.context.get('request')
        user = request.user if request else None

        if value.is_expired():
            raise serializers.ValidationError("Payment method is expired.")

        if value.user != user:
            raise serializers.ValidationError("This payment method does not belong to you.")

        return value

    def validate_project(self, value: Project):
        if not value.is_active:
            raise serializers.ValidationError("Project is already closed.")
        return value

    def validate(self, data):
        payment_method = data.get('payment_method')
        input_cvv = data.pop('cvv', None)
        user = self.context['request'].user
        project = data.get('project')

        if not payment_method or not input_cvv:
            raise serializers.ValidationError("CVV is required.")

        try:
            stored_cvv = payment_method.get_cvv()
        except Exception:
            raise serializers.ValidationError("Error verificating CVV number.")

        if str(stored_cvv) != str(input_cvv):
            raise serializers.ValidationError("CVV does not match the selected payment method.")

        if ProjectSponsorship.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError("This project is already featured.")

        return data

    def create(self, validated_data):
        validated_data['amount'] = 100
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)