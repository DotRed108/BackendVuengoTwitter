from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        post = Post.objects.create(author=author,
                                   parent_post=validated_data.get('parent_post'),
                                   content=validated_data.get('content'),
                                   image_content=validated_data.get('image_content')),
        return post

    class Meta:
        model = Post
        fields = ['content', 'parent_post', 'image_content']


class PostUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']
