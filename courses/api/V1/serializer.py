from rest_framework import serializers
from ...models import *
from accounts.models import CustomeUser, Profile


# class CourseApiSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=200)
#     price = serializers.IntegerField()


class CourseSerializer(serializers.ModelSerializer):
    #teacher = serializers.ReadOnlyField()
    content = serializers.ReadOnlyField()
    # detail_link = serializers.SerializerMethodField(method_name='detail')


    class Meta:
        model = Course
        fields = ["title", "price", "content", "category", "teacher", "image", 'status']

    
    # def detail(self,obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.id)
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['teacher'] = TrainerSerializer(instance.teacher).data
        rep['category'] = CategorySerializer(instance.category, many=True).data
        request = self.context.get('request')
        kwargs = request.parser_context.get('kwargs')
        if kwargs.get('pk') is not None:
            rep.pop('content')
        return rep
    
    def create(self, validated_data):
        #validated_data['teacher'] = self.context.get('request').user
        validated_data['content'] = 'for this course'
        return super().create(validated_data)

    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


        

class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ["id", "name"]



class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = '__all__'
