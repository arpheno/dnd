# Create your views here.
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from quests.models import Adventure, Quest


class AdventureSerializer(ModelSerializer):
    class Meta:
        model = Adventure
        fields = ('name','description','quests')
        depth = 3


class AdventureViewSet(ModelViewSet):
    queryset = Adventure.objects.all()
    serializer_class = AdventureSerializer


class QuestSerializer(ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'
        depth = 3


class QuestViewSet(ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
