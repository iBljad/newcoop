from haystack import indexes

from newcoop_app.models import GameRequest


class GameRequestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    game = indexes.CharField(model_attr='game')
    comment = indexes.CharField(model_attr='comment')
    platform = indexes.CharField(model_attr='platform')
    mic_present = indexes.BooleanField(model_attr='mic_present')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return GameRequest

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)
